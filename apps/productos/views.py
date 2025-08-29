from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from .models import Categoria, Medida
from django.urls import reverse_lazy
from django.http import JsonResponse

# Create your views here.
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria_list.html'
    context_object_name = 'categorias'

class CategoriaCreateView(CreateView):
    model = Categoria
    fields = ['categoria']
    template_name = 'categoria_form.html'  
    success_url = reverse_lazy('productos:categoria-list')  
    def form_valid(self, form):
        # Modifica el dato antes de guardar
        form.instance.habilitado = 1  
        form.instance.es_producto = 1  
        return super().form_valid(form)
    
class CategoriaUpdateView(UpdateView):
    model = Categoria
    fields = ['categoria', 'habilitado']
    template_name = 'categoria_form.html'  
    success_url = reverse_lazy('productos:categoria-list')

def categoria_detail(request, pk):
    categoria = Categoria.objects.get(pk=pk)
    data={
        "id": categoria.id,
        'categoria': categoria.categoria,
        'habilitado': categoria.habilitado,
        'es_producto': categoria.es_producto,        
    }
    return JsonResponse(data)


class MedidaListView(ListView):
    model = Medida
    template_name = 'medida_list.html'
    context_object_name = 'medidas'

class MedidaCreateView(CreateView):
    model = Medida
    fields = ['medida']
    template_name = 'medida_form.html'  # Not used for modal, but required
    success_url = reverse_lazy('productos:medida-list')  # Change to your list view

    def form_valid(self, form):
        form.instance.es_producto=1
        return super().form_valid(form)