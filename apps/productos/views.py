from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Categoria, Medida
from .forms import CategoriaForm, MedidaForm


# Create your views here.
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria_list.html'
    context_object_name = 'categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoriaForm()  # Añade el formulario al contexto
        return context

class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria_form.html'  
    success_url = reverse_lazy('productos:categoria-list')  
    def form_valid(self, form):
        # Modifica el dato antes de guardar
        form.instance.habilitado = 1  
        form.instance.es_producto = 1  
        return super().form_valid(form)
    
class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MedidaForm()  # Añade el formulario al contexto
        return context  

class MedidaCreateView(CreateView):
    model = Medida
    form_class = MedidaForm
    template_name = 'medida_form.html'  # Not used for modal, but required
    success_url = reverse_lazy('productos:medida-list')  # Change to your list view

    def form_valid(self, form):
        form.instance.es_producto=1
        return super().form_valid(form)
    
class MedidaUpdateView(UpdateView):
    model = Medida
    form_class = MedidaForm
    template_name = 'medida_form.html'  # Not used for modal, but required
    success_url = reverse_lazy('productos:medida-list')  # Change to your list view

def medida_detail(request, pk):
    medida = Medida.objects.get(pk=pk)
    data={
        "id": medida.id,
        'medida': medida.medida,             
    }
    return JsonResponse(data)