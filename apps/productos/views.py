from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Categoria, Medida, Derivado
from .forms import CategoriaForm, MedidaForm, DerivadoForm
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404
import logging
logger = logging.getLogger(__name__)


# Create your views here.
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria_list.html'
    context_object_name = 'categorias'
    paginate_by = 10  # Número de categorías por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoriaForm()  # Añade el formulario al contexto
        return context
    
    def get_queryset(self):        
        return Categoria.objects.filter(Q(eliminado=False) | Q(eliminado__isnull=True))

class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria_form.html'  
    success_url = reverse_lazy('productos:categoria-list')  
    
    def form_valid(self, form):
        # Modifica el dato antes de guardar
        form.instance.habilitado = 1  
        form.instance.es_producto = 1
        form.instance.eliminado = 0  
        
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            super().form_valid(form)
            return JsonResponse({'success': True, 'message': 'Categoría creada exitosamente'})
        else:
            return super().form_valid(form)
    
    def form_invalid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        else:
            return super().form_invalid(form)
    
class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categoria_form.html'  
    success_url = reverse_lazy('productos:categoria-list')
    
    def form_valid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            super().form_valid(form)
            return JsonResponse({'success': True, 'message': 'Categoría actualizada exitosamente'})
        else:
            return super().form_valid(form)
    
    def form_invalid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        else:
            return super().form_invalid(form)
    

def categoria_detail(request, pk):
    categoria = Categoria.objects.get(pk=pk)
    data={
        "id": categoria.id,
        'categoria': categoria.categoria,
        'habilitado': categoria.habilitado,
        'es_producto': categoria.es_producto,        
    }
    return JsonResponse(data)

def categoria_delete(request, pk):
    categoria = Categoria.objects.get(pk=pk)
    categoria.eliminado=1
    categoria.eliminado_ts=timezone.now()
    categoria.save()
    return redirect('productos:categoria-list')
    


class MedidaListView(ListView):
    model = Medida
    template_name = 'medida_list.html'
    context_object_name = 'medidas'
    paginate_by = 10  # Número de medidas por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MedidaForm()  # Añade el formulario al contexto
        return context  
    
    def get_queryset(self):        
        return Medida.objects.filter(Q(eliminado=False) | Q(eliminado__isnull=True))


class MedidaCreateView(CreateView):
    model = Medida
    form_class = MedidaForm
    template_name = 'medida_form.html'  # Not used for modal, but required
    success_url = reverse_lazy('productos:medida-list')  # Change to your list view

    def form_valid(self, form):
        form.instance.es_producto=1
        form.instance.habilitado=1
        form.instance.eliminado=0
        
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            super().form_valid(form)
            return JsonResponse({'success': True, 'message': 'Medida creada exitosamente'})
        else:
            return super().form_valid(form)
    
    def form_invalid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        else:
            return super().form_invalid(form)
    
class MedidaUpdateView(UpdateView):
    model = Medida
    form_class = MedidaForm
    template_name = 'medida_form.html'  # Not used for modal, but required
    success_url = reverse_lazy('productos:medida-list')  # Change to your list view
    
    def form_valid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            super().form_valid(form)
            return JsonResponse({'success': True, 'message': 'Medida actualizada exitosamente'})
        else:
            return super().form_valid(form)
    
    def form_invalid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        else:
            return super().form_invalid(form)

def medida_detail(request, pk):
    medida = Medida.objects.get(pk=pk)
    data={
        "id": medida.id,
        'medida': medida.medida,
        'habilitado': medida.habilitado             
    }
    return JsonResponse(data)

def medida_delete(request, pk):
    medida = Medida.objects.get(pk=pk)
    medida.eliminado=1
    medida.eliminado_ts=timezone.now()
    medida.save()
    return redirect('productos:medida-list')

class DerivadoListView(ListView):
    model = Derivado
    template_name = "derivados/_listado.html"
    context_object_name = "derivados"

    def get_queryset(self):
        return Derivado.objects.filter(medida_id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["medida_id"] = self.kwargs["pk"]
        return context

def get_derivados(request, pk):
    medida = Medida.objects.get(pk=pk)
    derivados = medida.derivado_set.all()  # Asumiendo que tienes una relación inversa desde Medida a Derivado
    data = {
        "medida": medida.medida,
        "derivados": [{"id": d.id, "derivado": d.derivado, "factorconversion": d.factorconversion} for d in derivados]
    }
    return JsonResponse(data)

class DerivadoCreateView(CreateView):
    model = Derivado
    form_class = DerivadoForm
    template_name = "temporales/form_derivado.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medida = get_object_or_404(Medida, pk=self.kwargs["pk"])
        context["medida"] = medida
        return context

    def form_valid(self, form):
        medida = get_object_or_404(Medida, pk=self.kwargs["pk"])
        derivado = form.save(commit=False)
        derivado.medida = medida
        derivado.save()
        return JsonResponse({"success": True})

    def form_invalid(self, form):
        logger.error("Errores al crear derivado: %s", form.errors)
        return JsonResponse({"success": False, "errors": form.errors})