# Create your models here.
import socket
from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    categoria = models.CharField(max_length=45, null=True, blank=True)
    habilitado = models.BooleanField(null=True)
    es_producto = models.BooleanField(null=True)
    eliminado_ts = models.DateTimeField(null=True, blank=True)
    eliminado = models.BooleanField(null=True)
    
    def __str__(self):
        return self.categoria or f"Categoría {self.id}"

class Medida(models.Model):
    medida = models.CharField(max_length=45, null=True, blank=True)
    habilitado = models.BooleanField(null=True)
    es_producto = models.BooleanField(null=True)
    eliminado_ts = models.DateTimeField(null=True, blank=True)
    eliminado = models.BooleanField(null=True)
    
    def __str__(self):
        return self.medida or f"Medida {self.id}"

class Derivado(models.Model):
    derivado = models.CharField(max_length=45, null=True, blank=True)
    medida = models.ForeignKey(Medida, on_delete=models.PROTECT)
    factorconversion = models.FloatField(null=True, blank=True)
    eliminado_ts = models.DateTimeField(null=True, blank=True)
    eliminado = models.BooleanField(null=True)

class Proveedor(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    nit = models.CharField(max_length=15, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    habilitado = models.BooleanField(null=True)
    es_producto = models.BooleanField(null=True)
    saldo = models.FloatField(null=True, blank=True)
    eliminado_ts = models.DateTimeField(null=True, blank=True)
    eliminado = models.BooleanField(null=True)
    
    def __str__(self):
        return self.nombre or f"Proveedor {self.id}"

class Producto(models.Model):  # Renombrado de Medicamento
    codigo = models.CharField(max_length=30, null=True, blank=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    nombregenerico = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    precio = models.FloatField(null=True, blank=True)
    habilitado = models.BooleanField(null=True)
    maximo = models.IntegerField(null=True, blank=True)
    minimo = models.IntegerField(null=True, blank=True)
    composicion = models.CharField(max_length=255, null=True, blank=True)
    presentacion = models.CharField(max_length=255, null=True, blank=True)
    es_producto = models.BooleanField(null=True)
    proveedor = models.ForeignKey(Proveedor, null=True, blank=True, on_delete=models.PROTECT)
    medida = models.ForeignKey(Medida, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.PROTECT)
    laboratorio_id = models.IntegerField(null=True, blank=True)  # Cambia por ForeignKey si tienes modelo Laboratorio
    eliminado_ts = models.DateTimeField(null=True, blank=True)
    eliminado = models.BooleanField(null=True)

class ProductoLugar(models.Model):  # Renombrado de MedicamentoLugar
    existencia = models.FloatField(null=True, blank=True)
    habilitado = models.BooleanField(null=True)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='productolugar_set')
    lugar = models.ForeignKey(
        'lugares.Lugar',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='productolugar_set',
        db_column='Lugar_idLugar',
    )


class Lote(models.Model):
    existencia = models.FloatField(null=True, blank=True)
    costo = models.FloatField(null=True, blank=True)
    costodescuento = models.FloatField(null=True, blank=True)
    fechaingreso = models.DateField(null=True, blank=True)
    terminado = models.FloatField(null=True, blank=True)
    lotetotal = models.FloatField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    productolugar = models.ForeignKey(ProductoLugar, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        skip_mov = getattr(self, "_skip_movimiento_primer_ingreso", False)
        super().save(*args, **kwargs)
        if is_new and not skip_mov:
            self._crear_movimientos_primer_ingreso()

    def _crear_movimientos_primer_ingreso(self):
        """
        Crea MovimientoProducto y MovimientoLote para ingreso manual del lote (sin compra).

        No asumir existencia 0 en ProductoLugar: puede haber stock previo de otros lotes
        o de ingresos anteriores. ultima_existencia = stock del lugar *antes* de este ingreso.
        """
        cantidad = (self.lotetotal is not None and self.lotetotal) or (self.existencia is not None and self.existencia) or 0
        costo = (self.costo is not None and self.costo) or 0
        try:
            host = socket.gethostname()
        except Exception:
            host = None

        # Valor real en BD (p. ej. ya hubo otro lote o movimiento antes de la primera compra)
        self.productolugar.refresh_from_db()
        ultima_pl_antes = float(self.productolugar.existencia or 0)

        mov = MovimientoProducto.objects.create(
            cant_entrada=cantidad,
            cant_salida=0,
            ultima_existencia=ultima_pl_antes,
            fechahora=timezone.now(),
            host=host,
            motivo='Primer_Ingreso',
            costo=costo,
            detalle_compra=None,
            productolugar=self.productolugar,
            detalle_factura_id=None,
            detalle_salida_id=None,
        )
        MovimientoLote.objects.create(
            cant_entrada=cantidad,
            cant_salida=0,
            ultima_existencia=0,
            lote=self,
            movimiento_producto=mov,
        )
        self.productolugar.existencia = ultima_pl_antes + float(cantidad)
        self.productolugar.save(update_fields=['existencia'])


class MovimientoProducto(models.Model):
    cant_entrada = models.FloatField(null=True, blank=True)
    cant_salida = models.FloatField(null=True, blank=True)
    ultima_existencia = models.FloatField(null=True, blank=True)
    fechahora = models.DateTimeField(null=True, blank=True)
    host = models.CharField(max_length=45, null=True, blank=True)
    motivo = models.CharField(max_length=255, null=True, blank=True)
    costo = models.FloatField(null=True, blank=True, default=0)
    detalle_compra = models.ForeignKey(
        "compras.DetalleCompra",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="movimientos_producto",
        db_column="DetalleCompra_id",
    )
    productolugar = models.ForeignKey(
        ProductoLugar,
        on_delete=models.PROTECT,
        related_name='movimientoproducto_set',
    )
    detalle_factura_id = models.BigIntegerField(null=True, blank=True)  # FK cuando exista DetalleFactura
    detalle_salida_id = models.BigIntegerField(null=True, blank=True)  # FK cuando exista DetalleSalida


class MovimientoLote(models.Model):
    cant_entrada = models.FloatField(null=True, blank=True)
    cant_salida = models.FloatField(null=True, blank=True)
    ultima_existencia = models.FloatField(null=True, blank=True)
    lote = models.ForeignKey(Lote, on_delete=models.PROTECT, related_name='movimientolote_set')
    movimiento_producto = models.ForeignKey(
        MovimientoProducto,
        on_delete=models.PROTECT,
        related_name='movimientolote_set',
    )


class MovimientoLugar(models.Model):
    cant_entrada = models.CharField(max_length=45, null=True, blank=True)
    entregado = models.BooleanField(null=True, blank=True)
    anulado = models.BooleanField(null=True, blank=True)
    movimiento_producto_origen = models.ForeignKey(
        MovimientoProducto,
        on_delete=models.PROTECT,
        related_name='movimientos_destino',
        db_column='MovimientoProducto_id_a_',
    )
    movimiento_producto_destino = models.ForeignKey(
        MovimientoProducto,
        on_delete=models.PROTECT,
        related_name='movimientos_origen',
        db_column='MovimientoProducto_id_b_',
    )
    detalle_factura_id = models.BigIntegerField(null=True, blank=True)  # FK cuando exista DetalleFactura