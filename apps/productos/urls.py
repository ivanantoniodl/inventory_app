from django.contrib import admin
from django.urls import path, include
from .views import CategoriaListView, CategoriaCreateView, MedidaCreateView,categoria_detail, CategoriaUpdateView
from .views import MedidaCreateView, medida_detail, MedidaListView, MedidaUpdateView
app_name = 'productos'

urlpatterns = [
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/create/', CategoriaCreateView.as_view(), name='categoria-create'),
    path('categoria/<int:pk>/', categoria_detail, name='categoria-detail'),
    path('categorias/update/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria-update'),
    path('medidas/', MedidaListView.as_view(), name='medida-list'),    
    path('medidas/create/', MedidaCreateView.as_view(), name='medida-create'),
    path('medidas/update/<int:pk>/', MedidaUpdateView.as_view(), name='medida-update'),
    path('medidas/<int:pk>/', medida_detail, name='medida-detail'),
    # Add other product-related URL patterns here
]