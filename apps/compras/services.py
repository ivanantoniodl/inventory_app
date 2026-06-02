"""Lógica de inventario al registrar/anular compras."""

from django.db import transaction
from django.utils import timezone

from apps.productos import inventory_services
from apps.productos.models import MovimientoLote
from apps.productos.models import MovimientoProducto


@transaction.atomic
def aplicar_detalle_compra_a_stock(detalle, request):
    return inventory_services.registrar_ingreso_compra_detalle(detalle, request=request)


@transaction.atomic
def anular_compra_y_revertir_stock(compra, request=None):
    """
    Anula una compra y registra los movimientos inversos de stock por cada detalle.

    Reglas:
    - Marca la compra como anulada.
    - Crea MovimientoProducto de salida por la cantidad del detalle.
    - Crea MovimientoLote sobre el lote que se creó al ingresar ese detalle.
    - Deja el lote anulado/terminado con existencia 0.
    - Resta la existencia del ProductoLugar.
    """
    compra = compra.__class__.objects.select_for_update().get(pk=compra.pk)
    if compra.anulada:
        return compra

    host = inventory_services.resolve_operation_host(request=request)
    ahora = timezone.now()
    factura = (compra.factura or "").strip() or str(compra.pk)

    detalles = (
        compra.detallecompra_set.select_for_update()
        .select_related("productolugar")
        .all()
        .order_by("id")
    )
    for detalle in detalles:
        cantidad = float(detalle.cantidad or 0)
        costo = float(detalle.costo or 0)
        pl = detalle.productolugar.__class__.objects.select_for_update().get(
            pk=detalle.productolugar_id
        )
        ultima_antes = float(pl.existencia or 0)

        if cantidad <= 0:
            continue
        if ultima_antes < cantidad:
            raise ValueError(
                f"No se puede anular la compra {compra.pk}: "
                f"el producto-lugar {pl.pk} tiene existencia insuficiente."
            )

        mov_ingreso = (
            detalle.movimientos_producto.filter(cant_entrada__gt=0)
            .order_by("-id")
            .first()
        )
        if mov_ingreso is None:
            raise ValueError(
                f"No se encontró el movimiento de ingreso para el detalle {detalle.pk}."
            )

        mov_lote_ingreso = (
            mov_ingreso.movimientolote_set.select_related("lote").order_by("-id").first()
        )
        if mov_lote_ingreso is None:
            raise ValueError(
                f"No se encontró el movimiento de lote para el detalle {detalle.pk}."
            )
        lote = mov_lote_ingreso.lote.__class__.objects.select_for_update().get(
            pk=mov_lote_ingreso.lote_id
        )

        mov_salida = MovimientoProducto.objects.create(
            cant_entrada=0,
            cant_salida=cantidad,
            ultima_existencia=ultima_antes,
            fechahora=ahora,
            host=host,
            motivo=f"Devolución Compra Factura {factura}"[:255],
            costo=costo,
            detalle_compra=detalle,
            productolugar=pl,
            detalle_factura_id=None,
            detalle_salida_id=None,
        )
        MovimientoLote.objects.create(
            cant_entrada=0,
            cant_salida=cantidad,
            ultima_existencia=float(lote.existencia or 0),
            lote=lote,
            movimiento_producto=mov_salida,
        )

        lote.existencia = 0
        lote.terminado = 1
        lote.save(update_fields=["existencia", "terminado"])

        pl.existencia = ultima_antes - cantidad
        pl.save(update_fields=["existencia"])

        detalle.cant_devuelta = cantidad
        detalle.anulada = True
        detalle.save(update_fields=["cant_devuelta", "anulada"])

    compra.anulada = True
    compra.saldo = 0
    compra.save(update_fields=["anulada", "saldo"])
    return compra
