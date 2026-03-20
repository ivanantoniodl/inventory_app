import json
from datetime import datetime

from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView

from apps.lugares.models import Lugar
from apps.productos.models import Producto
from apps.productos.models import ProductoLugar

from .forms import CompraCreateForm
from .forms import ProveedorForm
from .models import Compra
from .models import DetalleCompra
from .models import Proveedor
from .services import aplicar_detalle_compra_a_stock


class ProveedorListView(ListView):
    model = Proveedor
    template_name = "compras_proveedores.html"
    context_object_name = "proveedores"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProveedorForm()
        context["filtro_search"] = self.request.GET.get("search", "")
        return context

    def get_queryset(self):
        qs = Proveedor.objects.filter(Q(eliminado=False) | Q(eliminado__isnull=True))
        search = self.request.GET.get("search", "").strip()
        if search:
            qs = qs.filter(nombre__icontains=search)
        return qs.order_by("nombre")

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            tbody_html = render_to_string("compras_proveedores_tbody_rows.html", context)
            pagination_html = render_to_string("compras_proveedores_pagination.html", context)
            return JsonResponse({"tbody": tbody_html, "pagination": pagination_html})
        return self.render_to_response(context)


class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    success_url = reverse_lazy("compras:proveedor-list")

    def form_valid(self, form):
        if form.instance.habilitado is None:
            form.instance.habilitado = True
        form.instance.eliminado = False
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            super().form_valid(form)
            return JsonResponse({"success": True, "message": "Proveedor creado exitosamente"})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        return super().form_invalid(form)


class ProveedorUpdateView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    success_url = reverse_lazy("compras:proveedor-list")

    def form_valid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            super().form_valid(form)
            return JsonResponse({"success": True, "message": "Proveedor actualizado exitosamente"})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        return super().form_invalid(form)


def proveedor_detail(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    return JsonResponse(
        {
            "id": proveedor.id,
            "nombre": proveedor.nombre,
            "contacto": proveedor.contacto,
            "direccion": proveedor.direccion,
            "nit": proveedor.nit,
            "observaciones": proveedor.observaciones,
            "habilitado": proveedor.habilitado,
        }
    )


def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    proveedor.eliminado = True
    proveedor.eliminado_ts = timezone.now()
    proveedor.save(update_fields=["eliminado", "eliminado_ts"])
    return redirect("compras:proveedor-list")


class CompraListView(ListView):
    model = Compra
    template_name = "compras_list.html"
    context_object_name = "compras"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["proveedores"] = Proveedor.objects.filter(
            Q(eliminado=False) | Q(eliminado__isnull=True)
        ).order_by("nombre")
        context["filtro_fecha_desde"] = self.request.GET.get("fecha_desde", "")
        context["filtro_fecha_hasta"] = self.request.GET.get("fecha_hasta", "")
        context["filtro_anulada"] = self.request.GET.get("anulada", "")
        context["filtro_credito"] = self.request.GET.get("credito", "")
        context["filtro_proveedor"] = self.request.GET.get("proveedor", "")
        return context

    def get_queryset(self):
        qs = (
            Compra.objects.select_related("proveedor", "lugar")
            .filter(
                Q(proveedor__eliminado=False) | Q(proveedor__eliminado__isnull=True)
            )
            .order_by("-fechahora")
        )

        fecha_desde = self.request.GET.get("fecha_desde", "").strip()
        if fecha_desde:
            qs = qs.filter(fechahora__date__gte=fecha_desde)

        fecha_hasta = self.request.GET.get("fecha_hasta", "").strip()
        if fecha_hasta:
            qs = qs.filter(fechahora__date__lte=fecha_hasta)

        anulada = self.request.GET.get("anulada", "").strip()
        if anulada in {"0", "1"}:
            qs = qs.filter(anulada=bool(int(anulada)))

        credito = self.request.GET.get("credito", "").strip()
        if credito in {"0", "1"}:
            qs = qs.filter(credito=bool(int(credito)))

        proveedor_id = self.request.GET.get("proveedor", "").strip()
        if proveedor_id:
            qs = qs.filter(proveedor_id=proveedor_id)

        return qs


def _get_default_lugar():
    return Lugar.objects.order_by("idLugar").first()


def _resolve_lugar(selected_lugar):
    if selected_lugar is not None:
        return selected_lugar
    return _get_default_lugar()


def _build_catalog_product_options(limit=400):
    """Lista de productos activos para el JSON inicial del formulario (autocomplete también usa catálogo)."""
    options = []
    qs = (
        Producto.objects.filter(Q(eliminado=False) | Q(eliminado__isnull=True))
        .order_by("nombre")[:limit]
    )
    for p in qs:
        options.append(
            {
                "producto_id": p.id,
                "codigo": p.codigo or "",
                "nombre": p.nombre or f"Producto {p.id}",
                "precio": p.precio or 0,
            }
        )
    return options


def _next_factura():
    last = Compra.objects.order_by("-id").first()
    next_id = 1 if last is None else last.id + 1
    return str(next_id).zfill(8)[:8]


def productos_autocomplete(request):
    query = request.GET.get("q", "").strip()
    qs = Producto.objects.filter(Q(eliminado=False) | Q(eliminado__isnull=True))
    if query:
        qs = qs.filter(Q(nombre__icontains=query) | Q(codigo__icontains=query))
    qs = qs.order_by("nombre")[:40]

    results = []
    for p in qs:
        results.append(
            {
                "producto_id": p.id,
                "codigo": p.codigo or "",
                "nombre": p.nombre or f"Producto {p.id}",
                "precio": p.precio or 0,
            }
        )
    return JsonResponse({"results": results})


def compra_create(request):
    default_lugar = _get_default_lugar()
    selected_lugar = None
    current_lugar = default_lugar
    product_options = _build_catalog_product_options()
    initial_items_json = "[]"

    if request.method == "POST":
        form = CompraCreateForm(request.POST)
        raw_items = request.POST.get("items_json", "[]")
        initial_items_json = raw_items
        selected_lugar = form.data.get("lugar")
        if selected_lugar:
            try:
                selected_lugar = Lugar.objects.get(pk=int(selected_lugar))
            except (ValueError, Lugar.DoesNotExist):
                selected_lugar = None
        else:
            selected_lugar = None
        current_lugar = _resolve_lugar(selected_lugar)

        if current_lugar is None:
            messages.error(
                request,
                "No existe un Lugar configurado para registrar la compra.",
            )
            return render(
                request,
                "compras_form.html",
                {
                    "form": form,
                    "product_options": product_options,
                    "initial_items_json": initial_items_json,
                    "default_lugar": default_lugar,
                    "current_lugar": current_lugar,
                },
            )

        if form.is_valid():
            try:
                items = json.loads(raw_items)
            except json.JSONDecodeError:
                items = None

            if not isinstance(items, list) or len(items) == 0:
                messages.error(request, "Debe agregar al menos un producto a la compra.")
                return render(
                    request,
                    "compras_form.html",
                    {
                        "form": form,
                        "product_options": product_options,
                        "initial_items_json": initial_items_json,
                        "default_lugar": default_lugar,
                        "current_lugar": current_lugar,
                    },
                )

            normalized = []
            for item in items:
                if not isinstance(item, dict):
                    messages.error(request, "Formato inválido de items.")
                    return render(
                        request,
                        "compras_form.html",
                        {
                            "form": form,
                            "product_options": product_options,
                            "initial_items_json": initial_items_json,
                            "default_lugar": default_lugar,
                            "current_lugar": current_lugar,
                        },
                    )
                producto_id = item.get("producto_id")
                cantidad = item.get("cantidad")
                try:
                    producto_id = int(producto_id)
                    cantidad = float(cantidad)
                except (TypeError, ValueError):
                    messages.error(request, "Los items tienen valores inválidos.")
                    return render(
                        request,
                        "compras_form.html",
                        {
                            "form": form,
                            "product_options": product_options,
                            "initial_items_json": initial_items_json,
                            "default_lugar": default_lugar,
                            "current_lugar": current_lugar,
                        },
                    )
                if cantidad <= 0:
                    messages.error(request, "La cantidad debe ser mayor a 0.")
                    return render(
                        request,
                        "compras_form.html",
                        {
                            "form": form,
                            "product_options": product_options,
                            "initial_items_json": initial_items_json,
                            "default_lugar": default_lugar,
                            "current_lugar": current_lugar,
                        },
                    )
                normalized.append({"producto_id": producto_id, "cantidad": cantidad})

            selected_lugar = form.cleaned_data.get("lugar")
            current_lugar = _resolve_lugar(selected_lugar)
            for item in normalized:
                pid = item["producto_id"]
                if not Producto.objects.filter(
                    pk=pid
                ).filter(Q(eliminado=False) | Q(eliminado__isnull=True)).exists():
                    messages.error(
                        request,
                        f"El producto con id {pid} no existe o no está disponible.",
                    )
                    return render(
                        request,
                        "compras_form.html",
                        {
                            "form": form,
                            "product_options": product_options,
                            "initial_items_json": initial_items_json,
                            "default_lugar": default_lugar,
                            "current_lugar": current_lugar,
                        },
                    )

            with transaction.atomic():
                provider = form.cleaned_data["proveedor"]
                fecha = form.cleaned_data["fecha"]
                fecha_dt = datetime.combine(fecha, timezone.localtime().time())

                compra = Compra.objects.create(
                    proveedor=provider,
                    fechahora=fecha_dt,
                    factura=_next_factura(),
                    total=0,
                    anulada=False,
                    credito=False,
                    host=request.get_host()[:45] if request.get_host() else None,
                    lugar=current_lugar,
                    saldo=0,
                )

                total = 0
                for item in normalized:
                    producto_id = item["producto_id"]
                    cantidad = item["cantidad"]
                    producto = Producto.objects.get(pk=producto_id)
                    pl, _created_pl = ProductoLugar.objects.get_or_create(
                        producto=producto,
                        lugar=current_lugar,
                        defaults={
                            "existencia": 0,
                            "habilitado": True,
                        },
                    )
                    precio_base = producto.precio or 0
                    subtotal = float(precio_base) * float(cantidad)

                    detalle = DetalleCompra.objects.create(
                        compra=compra,
                        productolugar=pl,
                        cantidad=cantidad,
                        costo=precio_base,
                        subtotal=subtotal,
                        precio=precio_base,
                        precioventa=precio_base,
                        cant_devuelta=0,
                        anulada=False,
                    )
                    aplicar_detalle_compra_a_stock(detalle, request)
                    total += subtotal

                compra.total = total
                compra.saldo = total
                compra.save(update_fields=["total", "saldo"])

            messages.success(request, "Compra creada exitosamente.")
            return redirect("compras:compra-list")
    else:
        form = CompraCreateForm(initial={"fecha": timezone.localdate()})
        current_lugar = _resolve_lugar(form.initial.get("lugar"))
        product_options = _build_catalog_product_options()

    return render(
        request,
        "compras_form.html",
        {
            "form": form,
            "product_options": product_options,
            "initial_items_json": initial_items_json,
            "default_lugar": default_lugar,
            "current_lugar": current_lugar,
        },
    )
