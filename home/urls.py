from django.contrib import admin
from django.urls import path, include
from .views import HomeView,VentaView

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='homeapp'),
    path('ventas/', VentaView.as_view(), name='ventasapp'),
    # Include other app URLs here
]