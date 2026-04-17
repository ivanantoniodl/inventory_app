"""
Lógica de inventario al registrar/anular compras.
"""
import socket

from django.db import transaction
from django.utils import timezone

from apps.productos.models import Lote
from apps.productos.models import MovimientoLote
from apps.productos.models import MovimientoProducto


def _resolve_host(request):
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


def aplicar_detalle_compra_a_stock(detalle, request):
    """
    Tras crear un DetalleCompra:
    - Crea Lote (sin movimientos automáticos de primer ingreso).
    - Crea MovimientoProducto vinculado al detalle.
    - Crea MovimientoLote.
    - Actualiza existencia del ProductoLugar (ultima_existencia del movimiento = existencia antes del ingreso).
    """
    compra = detalle.compra
    pl = detalle.productolugar
    cantidad = float(detalle.cantidad or 0)
    costo = float(detalle.costo or 0)

    # Stock real antes de esta compra (p. ej. ya existía lote inicial vía Primer_Ingreso)
    pl.refresh_from_db()
    ultima_antes = float(pl.existencia or 0)

    fecha_ingreso = compra.fechahora.date() if compra.fechahora else None

    lote = Lote(
        existencia=cantidad,
        costo=costo,
        costodescuento=0,
        fechaingreso=fecha_ingreso,
        terminado=0,
        lotetotal=cantidad,
        fecha_vencimiento=None,
        productolugar=pl,
    )
    lote._skip_movimiento_primer_ingreso = True
    lote.save()

    factura = (compra.factura or "").strip() or str(compra.pk)
    motivo = f"Ingreso compra Factura {factura}"

    host = _resolve_host(request)

    mov = MovimientoProducto.objects.create(
        cant_entrada=cantidad,
        cant_salida=0,
        ultima_existencia=ultima_antes,
        fechahora=compra.fechahora,
        host=host,
        motivo=motivo[:255],
        costo=costo,
        detalle_compra=detalle,
        productolugar=pl,
        detalle_factura_id=None,
        detalle_salida_id=None,
    )

    MovimientoLote.objects.create(
        cant_entrada=cantidad,
        cant_salida=0,
        ultima_existencia=0,
        lote=lote,
        movimiento_producto=mov,
    )

    pl.existencia = ultima_antes + cantidad
    pl.save(update_fields=["existencia"])


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
    if compra.anulada:
        return compra

    host = _resolve_host(request)
    ahora = timezone.now()
    factura = (compra.factura or "").strip() or str(compra.pk)

    detalles = compra.detallecompra_set.select_related("productolugar").all().order_by("id")
    for detalle in detalles:
        cantidad = float(detalle.cantidad or 0)
        costo = float(detalle.costo or 0)
        pl = detalle.productolugar
        pl.refresh_from_db()
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
        lote = mov_lote_ingreso.lote

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
