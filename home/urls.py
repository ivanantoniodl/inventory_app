from django.contrib import admin
from django.urls import path, include
from .views import HomeView,VentaView, bienvenida,contacto,about

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='homeapp'),
    path('ventas/', VentaView.as_view(), name='ventasapp'),
    path('bienvenida/', bienvenida, name='bienvenida'),
    path('contacto/<str:correo>', contacto, name='contacto'),
    path('about/', about, name='about'),
    # Include other app URLs here
]