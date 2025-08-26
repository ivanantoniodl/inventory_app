from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

class VentaView(TemplateView):
    template_name = 'ventas.html'

