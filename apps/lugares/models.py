from django.db import models

# Create your models here.
from django.db import models


class LugarTipo(models.Model):
    idLugarTipo = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=25)
    eliminado_ts = models.DateTimeField(null=True, blank=True)
    eliminado = models.BooleanField(null=True)

    class Meta:
        db_table = 'LugarTipo'
        verbose_name = 'Tipo de Lugar'
        verbose_name_plural = 'Tipos de Lugar'

    def __str__(self):
        return self.tipo


class Empresa(models.Model):
    idEmpresa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45, null=True, blank=True)
    eliminado_ts = models.DateTimeField(null=True, blank=True)
    eliminado = models.BooleanField(null=True)

    class Meta:
        db_table = 'Empresa'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.nombre or f"Empresa {self.idEmpresa}"


class Lugar(models.Model):
    idLugar = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
        db_column='Empresa_idEmpresa',
        related_name='lugares'
    )
    lugar_tipo = models.ForeignKey(
        LugarTipo,
        on_delete=models.PROTECT,
        db_column='LugarTipo_idLugarTipo',
        related_name='lugares'
    )
    nombre = models.CharField(max_length=60, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=9, null=True, blank=True)
    num_placa = models.CharField(max_length=8, null=True, blank=True)
    eliminado_ts = models.DateTimeField(null=True, blank=True)
    eliminado = models.BooleanField(null=True)

    class Meta:
        db_table = 'Lugar'
        verbose_name = 'Lugar'
        verbose_name_plural = 'Lugares'
        indexes = [
            models.Index(fields=['lugar_tipo']),
            models.Index(fields=['empresa']),
        ]

    def __str__(self):
        return self.nombre or f"Lugar {self.idLugar}"