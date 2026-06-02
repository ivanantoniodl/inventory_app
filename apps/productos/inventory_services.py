import socket

from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from apps.productos.models import Lote
from apps.productos.models import MovimientoLote
from apps.productos.models import MovimientoProducto
from apps.productos.models import ProductoLugar


def resolve_operation_host(request=None, fallback_host=None):
    if fallback_host:
        return str(fallback_host)[:45]
    if request is not None:
        try:
            host = (request.get_host() or "")[:45]
            if host:
                return host
        except Exception:
            pass
    try:
        return (socket.gethostname() or "")[:45] or None
    except Exception:
        return None


@transaction.atomic
def registrar_ingreso_compra_detalle(detalle_compra, request=None, host=None):
    compra = detalle_compra.compra
    cantidad = float(detalle_compra.cantidad or 0)
    costo = float(detalle_compra.costo or 0)
    if cantidad <= 0:
        return None

    productolugar = ProductoLugar.objects.select_for_update().get(
        pk=detalle_compra.productolugar_id
    )
    existencia_antes = float(productolugar.existencia or 0)
    fecha_ingreso = compra.fechahora.date() if compra.fechahora else None

    lote = Lote(
        existencia=cantidad,
        costo=costo,
        costodescuento=0,
        fechaingreso=fecha_ingreso,
        terminado=0,
        lotetotal=cantidad,
        fecha_vencimiento=None,
        productolugar=productolugar,
    )
    lote._skip_movimiento_primer_ingreso = True
    lote.save()

    factura = (compra.factura or "").strip() or str(compra.pk)
    movimiento_producto = MovimientoProducto.objects.create(
        cant_entrada=cantidad,
        cant_salida=0,
        ultima_existencia=existencia_antes,
        fechahora=compra.fechahora,
        host=resolve_operation_host(request, host),
        motivo=f"Ingreso compra Factura {factura}"[:255],
        costo=costo,
        detalle_compra=detalle_compra,
        productolugar=productolugar,
        detalle_factura_id=None,
        detalle_salida_id=None,
    )

    MovimientoLote.objects.create(
        cant_entrada=cantidad,
        cant_salida=0,
        ultima_existencia=0,
        lote=lote,
        movimiento_producto=movimiento_producto,
    )

    productolugar.existencia = existencia_antes + cantidad
    productolugar.save(update_fields=["existencia"])
    return movimiento_producto


@transaction.atomic
def registrar_salida_venta_detalle(
    detalle_factura,
    *,
    nofactura,
    detalle_factura_id=None,
    request=None,
    host=None,
):
    cantidad_vendida = float(detalle_factura.cantidad or 0)
    if cantidad_vendida <= 0:
        return None

    productolugar = (
        ProductoLugar.objects.select_for_update()
        .select_related("producto")
        .get(pk=detalle_factura.productolugar_id)
    )
    existencia_antes = float(productolugar.existencia or 0)
    if existencia_antes < cantidad_vendida:
        raise ValueError(
            f"Existencia insuficiente para el producto '{productolugar.producto.nombre}'."
        )

    lotes = list(
        Lote.objects.select_for_update()
        .filter(productolugar=productolugar, existencia__gt=0)
        .filter(Q(terminado=0) | Q(terminado=False) | Q(terminado__isnull=True))
        .order_by("fechaingreso", "id")
    )
    if not lotes:
        raise ValueError(
            f"No hay lotes disponibles para el producto '{productolugar.producto.nombre}'."
        )

    restante = cantidad_vendida
    consumos = []
    costo_total = 0.0
    for lote in lotes:
        if restante <= 0:
            break
        existencia_lote = float(lote.existencia or 0)
        if existencia_lote <= 0:
            continue
        salida = min(restante, existencia_lote)
        consumos.append((lote, salida, existencia_lote))
        costo_total += salida * float(lote.costo or 0)
        restante -= salida

    if restante > 0:
        raise ValueError(
            f"Lotes insuficientes para cubrir la venta de '{productolugar.producto.nombre}'."
        )

    costo_promedio = (costo_total / cantidad_vendida) if cantidad_vendida > 0 else 0
    movimiento_producto = MovimientoProducto.objects.create(
        cant_entrada=0,
        cant_salida=cantidad_vendida,
        ultima_existencia=existencia_antes,
        fechahora=timezone.now(),
        host=resolve_operation_host(request, host),
        motivo=f"Ingreso de venta Factura {nofactura}"[:255],
        costo=costo_promedio,
        detalle_compra=None,
        productolugar=productolugar,
        detalle_factura_id=detalle_factura_id,
        detalle_salida_id=None,
    )

    for lote, salida_lote, ultima_lote in consumos:
        MovimientoLote.objects.create(
            cant_entrada=0,
            cant_salida=salida_lote,
            ultima_existencia=ultima_lote,
            lote=lote,
            movimiento_producto=movimiento_producto,
        )
        nueva_existencia = ultima_lote - salida_lote
        lote.existencia = nueva_existencia
        lote.terminado = 1 if nueva_existencia <= 0 else 0
        lote.save(update_fields=["existencia", "terminado"])

    productolugar.existencia = existencia_antes - cantidad_vendida
    productolugar.save(update_fields=["existencia"])
    return movimiento_producto


@transaction.atomic
def anular_venta_y_revertir_stock(factura, request=None, host=None):
    factura = factura.__class__.objects.select_for_update().get(pk=factura.pk)
    if factura.anulada:
        return factura

    detalles = factura.detallefactura_set.select_for_update().all().order_by("id")
    movimientos_salida = (
        MovimientoProducto.objects.select_for_update()
        .select_related("productolugar")
        .filter(
            detalle_factura_id=factura.id,
            cant_salida__gt=0,
            detalle_compra__isnull=True,
            detalle_salida_id__isnull=True,
        )
        .order_by("id")
    )
    if not movimientos_salida.exists():
        raise ValueError(
            f"No se encontraron movimientos de salida para anular la factura {factura.nofactura or factura.pk}."
        )

    host_value = resolve_operation_host(request=request, fallback_host=host)
    motivo = f"Anulación venta Factura {factura.nofactura or factura.pk}"[:255]
    ahora = timezone.now()

    for mov_salida in movimientos_salida:
        cantidad = float(mov_salida.cant_salida or 0)
        if cantidad <= 0:
            continue

        productolugar = ProductoLugar.objects.select_for_update().get(pk=mov_salida.productolugar_id)
        existencia_antes = float(productolugar.existencia or 0)

        mov_entrada = MovimientoProducto.objects.create(
            cant_entrada=cantidad,
            cant_salida=0,
            ultima_existencia=existencia_antes,
            fechahora=ahora,
            host=host_value,
            motivo=motivo,
            costo=float(mov_salida.costo or 0),
            detalle_compra=None,
            productolugar=productolugar,
            detalle_factura_id=factura.id,
            detalle_salida_id=None,
        )

        cantidad_reingresada = 0.0
        movs_lote_salida = (
            mov_salida.movimientolote_set.select_for_update()
            .select_related("lote")
            .all()
            .order_by("id")
        )
        for mov_lote_salida in movs_lote_salida:
            salida_lote = float(mov_lote_salida.cant_salida or 0)
            if salida_lote <= 0:
                continue
            lote = Lote.objects.select_for_update().get(pk=mov_lote_salida.lote_id)
            ultima_lote = float(lote.existencia or 0)
            MovimientoLote.objects.create(
                cant_entrada=salida_lote,
                cant_salida=0,
                ultima_existencia=ultima_lote,
                lote=lote,
                movimiento_producto=mov_entrada,
            )
            lote.existencia = ultima_lote + salida_lote
            lote.terminado = 0
            lote.save(update_fields=["existencia", "terminado"])
            cantidad_reingresada += salida_lote

        if cantidad_reingresada <= 0:
            raise ValueError(
                f"El movimiento de salida {mov_salida.id} no tiene lotes para revertir."
            )

        productolugar.existencia = existencia_antes + cantidad_reingresada
        productolugar.save(update_fields=["existencia"])

    for detalle in detalles:
        cantidad = float(detalle.cantidad or 0)
        detalle.anulado = True
        detalle.cantidad_devuelta = cantidad
        detalle.cantidad_devuelta_real = cantidad
        detalle.save(update_fields=["anulado", "cantidad_devuelta", "cantidad_devuelta_real"])

    factura.anulada = True
    factura.save(update_fields=["anulada"])
    return factura
