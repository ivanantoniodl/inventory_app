from django.contrib import admin
from django.urls import path, include
from .views import CategoriaListView, MedidaListView

app_name = 'products'

urlpatterns = [
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('medidas/', MedidaListView.as_view(), name='medida-list'),
    # Add other product-related URL patterns here
]