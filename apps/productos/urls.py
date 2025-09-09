from django.contrib import admin
from django.urls import path, include
from .views import CategoriaListView, CategoriaCreateView,categoria_detail, CategoriaUpdateView, categoria_delete
from .views import MedidaCreateView, medida_detail, MedidaListView, MedidaUpdateView, medida_delete
from .views import get_derivados,DerivadoCreateView, DerivadoListView
app_name = 'productos'

urlpatterns = [
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/create/', CategoriaCreateView.as_view(), name='categoria-create'),
    path('categoria/<int:pk>/', categoria_detail, name='categoria-detail'),
    path('categorias/update/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categoria/delete/<int:pk>/', categoria_delete, name='categoria-delete'),
    path('medidas/', MedidaListView.as_view(), name='medida-list'),    
    path('medidas/create/', MedidaCreateView.as_view(), name='medida-create'),
    path('medidas/update/<int:pk>/', MedidaUpdateView.as_view(), name='medida-update'),
    path('medidas/<int:pk>/', medida_detail, name='medida-detail'),
    path('medidas/delete/<int:pk>/', medida_delete, name='medida-delete'),
    path('medidas/<int:pk>/derivados/', get_derivados, name='medida-derivados'),
    path('medida/<int:pk>/derivados/crear/', DerivadoCreateView.as_view(), name='crear-derivado'),
    
    # Add other product-related URL patterns here
]