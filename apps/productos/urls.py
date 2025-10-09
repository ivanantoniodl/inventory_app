from django.contrib import admin
from django.urls import path, include
from .views import CategoriaListView, CategoriaCreateView,categoria_detail, CategoriaUpdateView, categoria_delete
from .views import MedidaCreateView, medida_detail, MedidaListView, MedidaUpdateView, medida_delete
from .views import get_derivados,DerivadoCreateView, DerivadoListView, DerivadosDeleteView
from .views import ProveedorListView, ProveedorCreateView, ProveedorUpdateView, proveedor_detail, proveedor_delete
from .views import ProductoListView, ProductoCreateView, ProductoUpdateView, producto_detail, producto_delete, producto_lotes
app_name = 'productos'

urlpatterns = [
    #Categorías URLs
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/create/', CategoriaCreateView.as_view(), name='categoria-create'),
    path('categoria/<int:pk>/', categoria_detail, name='categoria-detail'),
    path('categorias/update/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categoria/delete/<int:pk>/', categoria_delete, name='categoria-delete'),
    #Medidas URLs
    path('medidas/', MedidaListView.as_view(), name='medida-list'),    
    path('medidas/create/', MedidaCreateView.as_view(), name='medida-create'),
    path('medidas/update/<int:pk>/', MedidaUpdateView.as_view(), name='medida-update'),
    path('medidas/<int:pk>/', medida_detail, name='medida-detail'),
    path('medidas/delete/<int:pk>/', medida_delete, name='medida-delete'),
    path('medidas/<int:pk>/derivados/', get_derivados, name='medida-derivados'),
    #Derivados URLs
    path('medida/<int:pk>/derivados/crear/', DerivadoCreateView.as_view(), name='crear-derivado'),
    path('derivados/delete/<int:pk>/', DerivadosDeleteView.as_view(), name='delete-derivado'),
    #Proveedores URLs
    path('proveedores/', ProveedorListView.as_view(), name='proveedor-list'),
    path('proveedores/create/', ProveedorCreateView.as_view(), name='proveedor-create'),
    path('proveedores/update/<int:pk>/', ProveedorUpdateView.as_view(), name='proveedor-update'),
    path('proveedores/<int:pk>/', proveedor_detail, name='proveedor-detail'),
    path('proveedores/delete/<int:pk>/', proveedor_delete, name='proveedor-delete'),
    #Productos URLs
    path('productos/', ProductoListView.as_view(), name='producto-list'),
    path('productos/create/', ProductoCreateView.as_view(), name='producto-create'),
    path('productos/update/<int:pk>/', ProductoUpdateView.as_view(), name='producto-update'),
    path('productos/<int:pk>/', producto_detail, name='producto-detail'),
    path('productos/delete/<int:pk>/', producto_delete, name='producto-delete'),
    path('productos/<int:pk>/lotes/', producto_lotes, name='producto-lotes'),
    
    # Add other product-related URL patterns here
]