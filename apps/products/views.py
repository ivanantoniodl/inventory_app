from django.shortcuts import render
from django.views.generic import ListView
from .models import Categoria, Medida

# Create your views here.
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria_list.html'
    context_object_name = 'categorias'

class MedidaListView(ListView):
    model = Medida
    template_name = 'medida_list.html'
    context_object_name = 'medidas'