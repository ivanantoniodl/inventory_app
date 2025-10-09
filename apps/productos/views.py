from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Categoria, Medida, Derivado, Proveedor, Producto
from .forms import CategoriaForm, MedidaForm, DerivadoForm, ProveedorForm, ProductoForm
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

class DerivadosDeleteView(DeleteView):
    def post(self, request, pk, *args, **kwargs):
        derivado = get_object_or_404(Derivado, pk=pk)
        derivado.delete()
        return JsonResponse({"success": True})
    

class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'proveedores.html'
    context_object_name = 'proveedores'
    paginate_by = 10  # Número de proveedores por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProveedorForm()  # Añade el formulario al contexto
        return context  
    
    def get_queryset(self):        
        return Proveedor.objects.filter(Q(eliminado=False) | Q(eliminado__isnull=True))
    
class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor_form.html'  
    success_url = reverse_lazy('productos:proveedor-list')  
    
    def form_valid(self, form):
        # Modifica el dato antes de guardar
        form.instance.habilitado = 1  
        form.instance.es_producto = 1
        form.instance.eliminado = 0  
        form.instance.saldo = 0.0
        
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            super().form_valid(form)
            return JsonResponse({'success': True, 'message': 'Proveedor creado exitosamente'})
        else:
            return super().form_valid(form)
    
    def form_invalid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        else:
            return super().form_invalid(form)
        
class ProveedorUpdateView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor_form.html'  
    success_url = reverse_lazy('productos:proveedor-list')
    
    def form_valid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            super().form_valid(form)
            return JsonResponse({'success': True, 'message': 'Proveedor actualizado exitosamente'})
        else:
            return super().form_valid(form)
    
    def form_invalid(self, form):
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        else:
            return super().form_invalid(form)
        
def proveedor_detail(request, pk):
    proveedor = Proveedor.objects.get(pk=pk)
    data={
        "id": proveedor.id,
        'nombre': proveedor.nombre,
        'contacto': proveedor.contacto,
        'direccion': proveedor.direccion,
        'nit': proveedor.nit,
        'observaciones': proveedor.observaciones,
        'habilitado': proveedor.habilitado,
        'es_producto': proveedor.es_producto,        
    }
    return JsonResponse(data)

def proveedor_delete(request, pk):
    proveedor = Proveedor.objects.get(pk=pk)
    proveedor.eliminado=1
    proveedor.eliminado_ts=timezone.now()
    proveedor.save()
    return redirect('productos:proveedor-list')


class ProductoListView(ListView):
    model = Producto
    template_name = 'productos.html'
    context_object_name = 'productos'
    paginate_by = 10  # Número de productos por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductoForm()  # Añade el formulario al contexto
        return context  
    
    def get_queryset(self):        
        return Producto.objects.filter(Q(eliminado=False) | Q(eliminado__isnull=True))  

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto_form.html'  
    success_url = reverse_lazy('productos:producto-list')

    def form_valid(self, form):
        # Modifica el dato antes de guardar
        form.instance.habilitado = 1  
        form.instance.es_producto = 1
        form.instance.eliminado = 0  
        
        # Check if request is AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            super().form_valid(form)
            return JsonResponse({'success': True, 'message': 'Producto creado exitosamente'})
        else:
            return super().form_valid(form)
        
class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto_form.html'  
    success_url = reverse_lazy('productos:producto-list')
    
    def form_valid(self, form):
        # Check if request is AJAX
        form.instance.es_producto = 1
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            super().form_valid(form)
            return JsonResponse({'success': True, 'message': 'Producto actualizado exitosamente'})
        else:
            return super().form_valid(form)
        
def producto_detail(request, pk):
    producto = Producto.objects.get(pk=pk)
    data={
        "id": producto.id,
        'codigo': producto.codigo,
        'nombre': producto.nombre,
        'nombregenerico': producto.nombregenerico,
        'descripcion': producto.descripcion,
        'precio': producto.precio,
        'habilitado': producto.habilitado,
        'maximo': producto.maximo,
        'minimo': producto.minimo,
        'composicion': producto.composicion,
        'presentacion': producto.presentacion,
        'es_producto': producto.es_producto,        
        'proveedor': producto.proveedor.id if producto.proveedor else None,
        'medida': producto.medida.id if producto.medida else None,
        'categoria': producto.categoria.id if producto.categoria else None,
    }
    return JsonResponse(data)

def producto_delete(request, pk):
    producto = Producto.objects.get(pk=pk)
    producto.eliminado=1
    producto.eliminado_ts=timezone.now()
    producto.save()
    return redirect('productos:producto-list')

def producto_lotes(request, pk):
    """Get all lotes for a specific producto"""
    from .models import Lote, ProductoLugar
    
    # Get the producto
    producto = get_object_or_404(Producto, pk=pk)
    
    # Get all ProductoLugar entries for this producto
    producto_lugares = ProductoLugar.objects.filter(producto=producto)
    
    # Get all lotes for these ProductoLugar entries
    lotes = Lote.objects.filter(productolugar__in=producto_lugares)
    
    # Build the response data
    lotes_data = []
    for lote in lotes:
        lotes_data.append({
            'id': lote.id,
            'existencia': lote.existencia,
            'costo': lote.costo,
            'costodescuento': lote.costodescuento,
            'fechaingreso': lote.fechaingreso.strftime('%Y-%m-%d') if lote.fechaingreso else None,
            'terminado': lote.terminado,
            'lotetotal': lote.lotetotal,
            'fecha_vencimiento': lote.fecha_vencimiento.strftime('%Y-%m-%d') if lote.fecha_vencimiento else None,
        })
    
    return JsonResponse({
        'producto': producto.nombre,
        'lotes': lotes_data
    })