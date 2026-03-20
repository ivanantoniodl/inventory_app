from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Categoria, Medida, Derivado, Proveedor, Producto, ProductoLugar
from apps.lugares.models import Lugar
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
        context['form'] = CategoriaForm()
        context['filtro_search'] = self.request.GET.get('search', '')
        return context

    def get_queryset(self):
        qs = Categoria.objects.filter(Q(eliminado=False) | Q(eliminado__isnull=True))
        search = self.request.GET.get('search', '').strip()
        if search:
            qs = qs.filter(categoria__icontains=search)
        return qs

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and not self.object_list:
            from django.http import Http404
            raise Http404
        context = self.get_context_data()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            tbody_html = render_to_string('categoria_tbody_rows.html', context)
            pagination_html = render_to_string('categoria_pagination.html', context)
            return JsonResponse({'tbody': tbody_html, 'pagination': pagination_html})
        return self.render_to_response(context)

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
        context['form'] = ProveedorForm()
        context['filtro_search'] = self.request.GET.get('search', '')
        return context

    def get_queryset(self):
        qs = Proveedor.objects.filter(Q(eliminado=False) | Q(eliminado__isnull=True))
        search = self.request.GET.get('search', '').strip()
        if search:
            qs = qs.filter(nombre__icontains=search)
        return qs

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and not self.object_list:
            from django.http import Http404
            raise Http404
        context = self.get_context_data()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            tbody_html = render_to_string('proveedores_tbody_rows.html', context)
            pagination_html = render_to_string('proveedores_pagination.html', context)
            return JsonResponse({'tbody': tbody_html, 'pagination': pagination_html})
        return self.render_to_response(context)
    
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
    model = ProductoLugar
    template_name = 'productos.html'
    context_object_name = 'productolugares'
    paginate_by = 10  # Número de filas por página

    def _lugares_filtro_qs(self):
        return Lugar.objects.filter(
            Q(eliminado=False) | Q(eliminado__isnull=True)
        ).order_by("nombre")

    def dispatch(self, request, *args, **kwargs):
        """Siempre exige un lugar válido: si falta o es inválido, redirige al primero (por nombre)."""
        lugares_qs = self._lugares_filtro_qs()
        first_lugar = lugares_qs.first()
        if first_lugar is None:
            return super().dispatch(request, *args, **kwargs)
        valid = {str(pk) for pk in lugares_qs.values_list("idLugar", flat=True)}
        lugar_param = (request.GET.get("lugar") or "").strip()
        if lugar_param not in valid:
            q = request.GET.copy()
            q["lugar"] = str(first_lugar.idLugar)
            q["page"] = "1"
            return HttpResponseRedirect(f"{reverse('productos:producto-list')}?{q.urlencode()}")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductoForm()  # Añade el formulario al contexto
        # Lugares activos para el filtro
        context['lugares_filtro'] = self._lugares_filtro_qs()
        context['filtro_lugar_id'] = self.request.GET.get("lugar", "")
        context['filtro_search'] = self.request.GET.get("search", "")
        return context

    def get_queryset(self):
        # Una fila por producto en el lugar seleccionado (nunca mezclar todos los lugares)
        qs = (
            ProductoLugar.objects
            .filter(Q(producto__eliminado=False) | Q(producto__eliminado__isnull=True))
            .select_related('producto', 'producto__proveedor', 'producto__medida', 'producto__categoria', 'lugar')
            .order_by('producto__nombre', 'producto__id')
        )
        lugar_id = self.request.GET.get("lugar")
        if not lugar_id:
            return ProductoLugar.objects.none()
        qs = qs.filter(lugar_id=lugar_id)
        search = self.request.GET.get("search", "").strip()
        if search:
            qs = qs.filter(producto__nombre__icontains=search)
        return qs

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and not self.object_list:
            from django.http import Http404
            raise Http404
        context = self.get_context_data()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            tbody_html = render_to_string('productos_tbody_rows.html', context)
            pagination_html = render_to_string('productos_pagination.html', context)
            return JsonResponse({'tbody': tbody_html, 'pagination': pagination_html})
        return self.render_to_response(context)

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
            # Crear ProductoLugar con existencia 0 y habilitado True
            lugar_id = self.request.POST.get('lugar')
            if lugar_id:
                ProductoLugar.objects.create(
                    producto=self.object,
                    lugar_id=int(lugar_id),
                    existencia=0,
                    habilitado=True,
                )
            return JsonResponse({'success': True, 'message': 'Producto creado exitosamente'})
        else:
            super().form_valid(form)
            lugar_id = self.request.POST.get('lugar')
            if lugar_id:
                ProductoLugar.objects.create(
                    producto=self.object,
                    lugar_id=int(lugar_id),
                    existencia=0,
                    habilitado=True,
                )
            return redirect(self.success_url)
        
class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto_form.html'  
    success_url = reverse_lazy('productos:producto-list')

    def form_valid(self, form):
        form.instance.es_producto = 1
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            super().form_valid(form)
            # Si se deshabilita el producto, deshabilitar también ProductoLugar
            if not form.instance.habilitado:
                ProductoLugar.objects.filter(producto=self.object).update(habilitado=False)
            return JsonResponse({'success': True, 'message': 'Producto actualizado exitosamente'})
        else:
            super().form_valid(form)
            if not form.instance.habilitado:
                ProductoLugar.objects.filter(producto=self.object).update(habilitado=False)
            return redirect(self.success_url)
        
def producto_detail(request, pk):
    producto = Producto.objects.get(pk=pk)
    productolugares = ProductoLugar.objects.filter(producto=producto).select_related('lugar')
    data = {
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
        'productolugares': [
            {
                'lugar_id': pl.lugar_id,
                'lugar_nombre': pl.lugar.nombre if pl.lugar else '—',
                'existencia': pl.existencia,
                'habilitado': pl.habilitado,
            }
            for pl in productolugares
        ],
    }
    return JsonResponse(data)

def producto_delete(request, pk):
    producto = Producto.objects.get(pk=pk)
    producto.eliminado=1
    producto.eliminado_ts=timezone.now()
    producto.save()
    return redirect('productos:producto-list')

def producto_lotes(request, pk):
    """Get lotes for a product. If productolugar_id in GET, filter by that ProductoLugar."""
    from .models import Lote, ProductoLugar

    producto = get_object_or_404(Producto, pk=pk)
    producto_lugares = ProductoLugar.objects.filter(producto=producto)

    productolugar_id = request.GET.get('productolugar_id', '').strip()
    if productolugar_id:
        try:
            pl = producto_lugares.get(pk=int(productolugar_id))
        except (ValueError, ProductoLugar.DoesNotExist):
            pl = None
        if pl is not None:
            lotes = Lote.objects.filter(productolugar=pl)
            productolugar_id_out = pl.id
        else:
            lotes = Lote.objects.filter(productolugar__in=producto_lugares)
            productolugar_id_out = None
    else:
        lotes = Lote.objects.filter(productolugar__in=producto_lugares)
        productolugar_id_out = None

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

    payload = {
        'producto': producto.nombre,
        'lotes': lotes_data,
    }
    if productolugar_id_out is not None:
        payload['productolugar_id'] = productolugar_id_out
    return JsonResponse(payload)


def lote_primer_ingreso(request, productolugar_pk):
    """POST: crea un Lote de primer ingreso para el ProductoLugar indicado."""
    from .models import Lote

    if request.method != 'POST':
        return JsonResponse({'success': False, 'errors': ['Método no permitido']}, status=405)

    productolugar = get_object_or_404(ProductoLugar, pk=productolugar_pk)

    existencia = request.POST.get('existencia')
    costo = request.POST.get('costo')
    fecha_vencimiento = request.POST.get('fecha_vencimiento')

    errors = []
    if existencia is None or existencia == '':
        errors.append('Existencia es requerida.')
    if costo is None or costo == '':
        errors.append('Costo es requerido.')
    if fecha_vencimiento is None or fecha_vencimiento == '':
        errors.append('Fecha de vencimiento es requerida.')

    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    try:
        existencia_f = float(existencia.replace(',', '.'))
        costo_f = float(costo.replace(',', '.'))
    except ValueError:
        return JsonResponse({'success': False, 'errors': ['Existencia y costo deben ser numéricos.']}, status=400)

    if existencia_f < 0:
        return JsonResponse({'success': False, 'errors': ['Existencia no puede ser negativa.']}, status=400)

    try:
        from datetime import datetime
        fecha_venc = datetime.strptime(fecha_vencimiento.strip(), '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'success': False, 'errors': ['Fecha de vencimiento inválida (use AAAA-MM-DD).']}, status=400)

    costodescuento = costo_f
    fechaingreso = timezone.now().date()

    lote = Lote.objects.create(
        existencia=existencia_f,
        costo=costo_f,
        costodescuento=costodescuento,
        fechaingreso=fechaingreso,
        terminado=0,
        lotetotal=existencia_f,
        fecha_vencimiento=fecha_venc,
        productolugar=productolugar,
    )

    return JsonResponse({
        'success': True,
        'lote': {
            'id': lote.id,
            'existencia': lote.existencia,
            'costo': lote.costo,
            'costodescuento': lote.costodescuento,
            'fechaingreso': lote.fechaingreso.strftime('%Y-%m-%d'),
            'fecha_vencimiento': lote.fecha_vencimiento.strftime('%Y-%m-%d'),
        },
    })