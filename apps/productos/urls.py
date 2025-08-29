from django.contrib import admin
from django.urls import path, include
from .views import CategoriaListView, MedidaListView, CategoriaCreateView, MedidaCreateView,categoria_detail

app_name = 'productos'

urlpatterns = [
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/create/', CategoriaCreateView.as_view(), name='categoria-create'),
    path('medidas/', MedidaListView.as_view(), name='medida-list'),    
    path('medidas/create/', MedidaCreateView.as_view(), name='medida-create'),
    path('categoria/<int:pk>/', categoria_detail, name='categoria-detail'),
    # Add other product-related URL patterns here
]