"""
Lógica de inventario al registrar una compra: Lote, movimientos y existencia en ProductoLugar.
"""
from apps.productos.models import Lote
from apps.productos.models import MovimientoLote
from apps.productos.models import MovimientoProducto


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

    host = None
    if request is not None:
        try:
            host = (request.get_host() or "")[:45] or None
        except Exception:
            host = None

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
