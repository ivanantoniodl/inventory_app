from django.urls import path

from .views import cliente_delete
from .views import cliente_detail
from .views import ClienteCreateView
from .views import ClienteListView
from .views import ClienteUpdateView
from .views import FacturaListView
from .views import productos_autocomplete
from .views import venta_anular
from .views import venta_create
from .views import venta_detail

app_name = "ventas"

urlpatterns = [
    path("clientes/", ClienteListView.as_view(), name="cliente-list"),
    path("clientes/create/", ClienteCreateView.as_view(), name="cliente-create"),
    path("clientes/update/<int:pk>/", ClienteUpdateView.as_view(), name="cliente-update"),
    path("clientes/<int:pk>/", cliente_detail, name="cliente-detail"),
    path("clientes/delete/<int:pk>/", cliente_delete, name="cliente-delete"),
    path("ventas/", FacturaListView.as_view(), name="venta-list"),
    path("ventas/nueva/", venta_create, name="venta-create"),
    path("ventas/<int:pk>/detalle/", venta_detail, name="venta-detail"),
    path("ventas/<int:pk>/anular/", venta_anular, name="venta-anular"),
    path("productos/autocomplete/", productos_autocomplete, name="productos-autocomplete"),
]
