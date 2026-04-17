from django.db import models


class TipoTel(models.Model):
    tipo = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.tipo or f"TipoTel {self.id}"


class Proveedor(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    contacto = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    nit = models.CharField(max_length=15, null=True, blank=True, unique=True)
    observaciones = models.TextField(null=True, blank=True)
    habilitado = models.BooleanField(null=True, blank=True)
    es_medicamento = models.BooleanField(null=True, blank=True)
    saldo = models.FloatField(null=True, blank=True)
    eliminado = models.BooleanField(null=True, blank=True)
    eliminado_ts = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre or f"Proveedor {self.id}"


class Telefono(models.Model):
    numero = models.CharField(max_length=13)
    tipotel = models.ForeignKey(TipoTel, on_delete=models.PROTECT, db_column="TipoTel_id")
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column="Proveedor_id",
    )
    cliente = models.ForeignKey(
        "ventas.Cliente",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column="Cliente_id",
    )

    def __str__(self):
        return self.numero


class Compra(models.Model):
    fechahora = models.DateTimeField()
    total = models.FloatField()
    factura = models.CharField(max_length=8)
    anulada = models.BooleanField(null=True, blank=True, default=False)
    credito = models.BooleanField(null=True, blank=True, default=False)
    usuario_id = models.BigIntegerField(null=True, blank=True)
    host = models.CharField(max_length=45, null=True, blank=True)
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        db_column="Proveedor_id",
    )
    lugar = models.ForeignKey(
        "lugares.Lugar",
        on_delete=models.PROTECT,
        db_column="Lugar_idLugar",
    )
    saldo = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Compra {self.id} - {self.factura}"


class DetalleCompra(models.Model):
    cantidad = models.FloatField(null=True, blank=True)
    costo = models.FloatField(null=True, blank=True)
    subtotal = models.FloatField(null=True, blank=True)
    precio = models.FloatField(null=True, blank=True)
    precioventa = models.FloatField(null=True, blank=True)
    cant_devuelta = models.FloatField(null=True, blank=True)
    anulada = models.BooleanField(null=True, blank=True)
    compra = models.ForeignKey(
        Compra,
        on_delete=models.PROTECT,
        db_column="Compra_id",
    )
    productolugar = models.ForeignKey(
        "productos.ProductoLugar",
        on_delete=models.PROTECT,
        db_column="ProductoLugar_id",
    )

    def __str__(self):
        return f"DetalleCompra {self.id}"
