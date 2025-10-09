from django.urls import path
from .views import (
    EmpresaListView, EmpresaCreateView, EmpresaUpdateView, empresa_detail, empresa_delete,
    LugarListView, LugarCreateView, LugarUpdateView, lugar_detail, lugar_delete
)

app_name = 'lugares'

urlpatterns = [
    # Empresas URLs
    path('empresas/', EmpresaListView.as_view(), name='empresa-list'),
    path('empresas/create/', EmpresaCreateView.as_view(), name='empresa-create'),
    path('empresas/<int:pk>/', empresa_detail, name='empresa-detail'),
    path('empresas/update/<int:pk>/', EmpresaUpdateView.as_view(), name='empresa-update'),
    path('empresas/delete/<int:pk>/', empresa_delete, name='empresa-delete'),
    
    # Lugares URLs
    path('lugares/', LugarListView.as_view(), name='lugar-list'),
    path('lugares/create/', LugarCreateView.as_view(), name='lugar-create'),
    path('lugares/<int:pk>/', lugar_detail, name='lugar-detail'),
    path('lugares/update/<int:pk>/', LugarUpdateView.as_view(), name='lugar-update'),
    path('lugares/delete/<int:pk>/', lugar_delete, name='lugar-delete'),
]
