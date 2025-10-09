from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Empresa, Lugar, LugarTipo
from .forms import EmpresaForm, LugarForm

# Create your views here.
class EmpresaListView(ListView):
    model = Empresa
    template_name = 'lugares/empresa_list.html'
    context_object_name = 'empresas'
    paginate_by = 10  # Número de empresas por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EmpresaForm()  # Añade el formulario al contexto
        return context
    
    def get_queryset(self):        
        return Empresa.objects.all().order_by('nombre')

class EmpresaCreateView(CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'lugares/empresa_form.html'  
    success_url = reverse_lazy('lugares:empresa-list')  
    
    def form_valid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            super().form_valid(form)
            return JsonResponse({'success': True, 'message': 'Empresa creada exitosamente'})
        else:
            return super().form_valid(form)
    
    def form_invalid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        else:
            return super().form_invalid(form)
    
class EmpresaUpdateView(UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'lugares/empresa_form.html'  
    success_url = reverse_lazy('lugares:empresa-list')
    
    def form_valid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            super().form_valid(form)
            return JsonResponse({'success': True, 'message': 'Empresa actualizada exitosamente'})
        else:
            return super().form_valid(form)
    
    def form_invalid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        else:
            return super().form_invalid(form)
    

def empresa_detail(request, pk):
    empresa = Empresa.objects.get(pk=pk)
    data={
        "id": empresa.idEmpresa,
        'nombre': empresa.nombre,
    }
    return JsonResponse(data)

def empresa_delete(request, pk):
    empresa = Empresa.objects.get(pk=pk)
    empresa.delete()
    return redirect('lugares:empresa-list')


# Lugar views
class LugarListView(ListView):
    model = Lugar
    template_name = 'lugares/lugar_list.html'
    context_object_name = 'lugares'
    paginate_by = 10  # Número de lugares por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LugarForm()  # Añade el formulario al contexto
        return context
    
    def get_queryset(self):        
        return Lugar.objects.all().order_by('nombre').select_related('empresa', 'lugar_tipo')

class LugarCreateView(CreateView):
    model = Lugar
    form_class = LugarForm
    template_name = 'lugares/lugar_form.html'  
    success_url = reverse_lazy('lugares:lugar-list')  
    
    def form_valid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            super().form_valid(form)
            return JsonResponse({'success': True, 'message': 'Lugar creado exitosamente'})
        else:
            return super().form_valid(form)
    
    def form_invalid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        else:
            return super().form_invalid(form)
        
class LugarUpdateView(UpdateView):
    model = Lugar
    form_class = LugarForm
    template_name = 'lugares/lugar_form.html'  
    success_url = reverse_lazy('lugares:lugar-list')
    
    def form_valid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            super().form_valid(form)
            return JsonResponse({'success': True, 'message': 'Lugar actualizado exitosamente'})
        else:
            return super().form_valid(form)
    
    def form_invalid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        else:
            return super().form_invalid(form)
        
def lugar_detail(request, pk):
    lugar = Lugar.objects.get(pk=pk)
    data={
        "id": lugar.idLugar,
        'empresa': lugar.empresa.nombre,
        'lugar_tipo': lugar.lugar_tipo.tipo,
        'nombre': lugar.nombre,
        'direccion': lugar.direccion,
        'telefono': lugar.telefono,
        'num_placa': lugar.num_placa,
    }
    return JsonResponse(data)

def lugar_delete(request, pk):
    lugar = Lugar.objects.get(pk=pk)
    lugar.delete()
    return redirect('lugares:lugar-list')