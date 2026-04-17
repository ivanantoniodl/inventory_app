from django.urls import path

from .views import compra_anular
from .views import compra_detail
from .views import compra_create
from .views import CompraListView
from .views import productos_autocomplete
from .views import ProveedorCreateView
from .views import ProveedorListView
from .views import ProveedorUpdateView
from .views import proveedor_delete
from .views import proveedor_detail

app_name = "compras"

urlpatterns = [
    path("proveedores/", ProveedorListView.as_view(), name="proveedor-list"),
    path("proveedores/create/", ProveedorCreateView.as_view(), name="proveedor-create"),
    path("proveedores/update/<int:pk>/", ProveedorUpdateView.as_view(), name="proveedor-update"),
    path("proveedores/<int:pk>/", proveedor_detail, name="proveedor-detail"),
    path("proveedores/delete/<int:pk>/", proveedor_delete, name="proveedor-delete"),
    path("compras/", CompraListView.as_view(), name="compra-list"),
    path("compras/nueva/", compra_create, name="compra-create"),
    path("compras/<int:pk>/detalle/", compra_detail, name="compra-detail"),
    path("compras/<int:pk>/anular/", compra_anular, name="compra-anular"),
    path("productos/autocomplete/", productos_autocomplete, name="productos-autocomplete"),
]
