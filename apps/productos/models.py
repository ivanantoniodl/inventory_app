# Create your models here.
from django.db import models

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