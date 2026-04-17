from django.contrib import admin

from .models import Cliente
from .models import DetalleFactura
from .models import DetallePagoCredito
from .models import DetalleSalida
from .models import Factura
from .models import LugarReq
from .models import Motivo
from .models import PagoCredito
from .models import Salida


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "apellido", "nit", "activo")
    search_fields = ("nombre", "apellido", "nit", "dpi")
    list_filter = ("activo",)


@admin.register(LugarReq)
class LugarReqAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "direccion", "telefono")
    search_fields = ("nombre", "direccion", "telefono")


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ("id", "nofactura", "fechahora", "cliente", "lugar", "total", "anulada")
    search_fields = ("nofactura", "nombrefactura", "nitfactura")
    list_filter = ("anulada", "entregada", "credito", "lugar")


@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = ("id", "factura", "productolugar", "derivado", "cantidad", "precioventa", "anulado")
    list_filter = ("anulado", "devolver")


@admin.register(Salida)
class SalidaAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "documentono", "usuario_id")
    search_fields = ("documentono",)


@admin.register(DetalleSalida)
class DetalleSalidaAdmin(admin.ModelAdmin):
    list_display = ("id", "salida", "productolugar", "derivado", "cantidad", "anulado")
    list_filter = ("anulado",)


@admin.register(Motivo)
class MotivoAdmin(admin.ModelAdmin):
    list_display = ("id", "motivo", "habilitado")
    search_fields = ("motivo",)
    list_filter = ("habilitado",)


@admin.register(PagoCredito)
class PagoCreditoAdmin(admin.ModelAdmin):
    list_display = ("id", "fechahora", "proveedor", "total", "anulado", "nodocumento")
    search_fields = ("nodocumento", "chequepago")
    list_filter = ("anulado",)


@admin.register(DetallePagoCredito)
class DetallePagoCreditoAdmin(admin.ModelAdmin):
    list_display = ("id", "compra", "pagocredito", "monto", "nofacturapagada")
    search_fields = ("nofacturapagada",)
