from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255, null=True, blank=True)
    direccion = models.CharField(max_length=255)
    email = models.CharField(max_length=45, null=True, blank=True)
    nit = models.CharField(max_length=13, null=True, blank=True, unique=True, db_index=True)
    activo = models.BooleanField(
        null=True,
        blank=True,
        help_text="1 Activo / 0 No Activo",
    )
    dpi = models.CharField(max_length=13, null=True, blank=True)

    class Meta:
        db_table = "Cliente"

    def __str__(self):
        return f"{self.nombre} {self.apellido or ''}".strip()


class LugarReq(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True, db_column="Nombre")
    direccion = models.CharField(max_length=100, null=True, blank=True, db_column="Direccion")
    telefono = models.CharField(max_length=100, null=True, blank=True, db_column="Telefono")

    class Meta:
        db_table = "LugarReq"

    def __str__(self):
        return self.nombre or f"LugarReq {self.pk}"


class Factura(models.Model):
    fechahora = models.DateTimeField(null=True, blank=True)
    usuario_id = models.BigIntegerField(null=True, blank=True)
    host = models.CharField(max_length=45, null=True, blank=True)
    anulada = models.BooleanField(null=True, blank=True, default=False)
    entregada = models.BooleanField(null=True, blank=True, default=False)
    total = models.FloatField(null=True, blank=True)
    credito = models.BooleanField(null=True, blank=True)
    nombrefactura = models.CharField(max_length=255, null=True, blank=True)
    direccionfactura = models.CharField(max_length=255, null=True, blank=True)
    nitfactura = models.CharField(max_length=15, null=True, blank=True)
    impresa = models.BooleanField(null=True, blank=True)
    nofactura = models.CharField(max_length=45, null=True, blank=True)
    refacturado = models.BooleanField(null=True, blank=True)
    clientesvarios = models.BooleanField(null=True, blank=True)
    lugar = models.ForeignKey(
        "lugares.Lugar",
        on_delete=models.PROTECT,
        db_column="Lugar_idLugar",
    )
    cliente = models.ForeignKey(
        "ventas.Cliente",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column="Cliente_id",
    )
    lugarreq = models.ForeignKey(
        "ventas.LugarReq",
        on_delete=models.PROTECT,
        db_column="LugarReq_id",
    )

    class Meta:
        db_table = "Factura"

    def __str__(self):
        return self.nofactura or f"Factura {self.pk}"


class DetalleFactura(models.Model):
    cantidad = models.FloatField(null=True, blank=True)
    cantidad_real = models.FloatField(null=True, blank=True)
    cantidad_entregada = models.FloatField(null=True, blank=True)
    cantidad_entregada_real = models.FloatField(null=True, blank=True)
    cantidad_devuelta = models.FloatField(null=True, blank=True)
    cantidad_devuelta_real = models.FloatField(null=True, blank=True)
    anulado = models.BooleanField(null=True, blank=True)
    devolver = models.BooleanField(null=True, blank=True)
    precionormal = models.FloatField(null=True, blank=True)
    precioventa = models.FloatField(null=True, blank=True)
    productolugar = models.ForeignKey(
        "productos.ProductoLugar",
        on_delete=models.PROTECT,
        db_column="MedicamentoLugar_id",
    )
    factura = models.ForeignKey(
        "ventas.Factura",
        on_delete=models.PROTECT,
        db_column="Factura_id",
    )
    derivado = models.ForeignKey(
        "productos.Derivado",
        on_delete=models.PROTECT,
        db_column="Derivado_id",
    )

    class Meta:
        db_table = "DetalleFactura"


class Salida(models.Model):
    fecha = models.DateTimeField(null=True, blank=True)
    usuario_id = models.BigIntegerField(null=True, blank=True)
    documentono = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = "Salida"


class DetalleSalida(models.Model):
    cantidad = models.FloatField(null=True, blank=True)
    cantidad_real = models.FloatField(null=True, blank=True)
    anulado = models.BooleanField(null=True, blank=True)
    motivo = models.TextField(null=True, blank=True)
    salida = models.ForeignKey(
        "ventas.Salida",
        on_delete=models.PROTECT,
        db_column="Salida_id",
    )
    productolugar = models.ForeignKey(
        "productos.ProductoLugar",
        on_delete=models.PROTECT,
        db_column="MedicamentoLugar_id",
    )
    derivado = models.ForeignKey(
        "productos.Derivado",
        on_delete=models.PROTECT,
        db_column="Derivado_id",
    )

    class Meta:
        db_table = "DetalleSalida"


class Motivo(models.Model):
    motivo = models.CharField(max_length=100, null=True, blank=True)
    habilitado = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = "Motivo"

    def __str__(self):
        return self.motivo or f"Motivo {self.pk}"


class PagoCredito(models.Model):
    fechahora = models.DateTimeField(null=True, blank=True, db_column="FechaHora")
    total = models.FloatField(null=True, blank=True, db_column="Total")
    anulado = models.BooleanField(null=True, blank=True, default=False, db_column="Anulado")
    nodocumento = models.CharField(max_length=45, null=True, blank=True, db_column="NoDocumento")
    chequepago = models.CharField(max_length=45, null=True, blank=True, db_column="ChequePago")
    proveedor = models.ForeignKey(
        "compras.Proveedor",
        on_delete=models.PROTECT,
        db_column="Proveedor_id",
    )

    class Meta:
        db_table = "PagoCredito"


class DetallePagoCredito(models.Model):
    compra = models.ForeignKey(
        "compras.Compra",
        on_delete=models.PROTECT,
        db_column="Compra_id",
    )
    pagocredito = models.ForeignKey(
        "ventas.PagoCredito",
        on_delete=models.PROTECT,
        db_column="PagoCredito_id",
    )
    monto = models.FloatField(null=True, blank=True, db_column="Monto")
    nofacturapagada = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_column="NoFacturaPagada",
    )

    class Meta:
        db_table = "DetallePagoCredito"
