import json
from datetime import datetime

from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView

from apps.lugares.models import Lugar
from apps.productos.models import Derivado
from apps.productos.models import ProductoLugar
from apps.productos import inventory_services

from .forms import ClienteForm
from .forms import VentaCreateForm
from .models import Cliente
from .models import DetalleFactura
from .models import Factura
from .models import LugarReq


class ClienteListView(ListView):
    model = Cliente
    template_name = "ventas_clientes.html"
    context_object_name = "clientes"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ClienteForm()
        context["filtro_search"] = self.request.GET.get("search", "")
        return context

    def get_queryset(self):
        qs = Cliente.objects.all().order_by("nombre", "apellido")
        search = self.request.GET.get("search", "").strip()
        if search:
            qs = qs.filter(Q(nombre__icontains=search) | Q(apellido__icontains=search))
        return qs

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            tbody_html = render_to_string("ventas_clientes_tbody_rows.html", context)
            pagination_html = render_to_string("ventas_clientes_pagination.html", context)
            return JsonResponse({"tbody": tbody_html, "pagination": pagination_html})
        return self.render_to_response(context)


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy("ventas:cliente-list")

    def form_valid(self, form):
        if form.instance.activo is None:
            form.instance.activo = True
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            super().form_valid(form)
            return JsonResponse({"success": True, "message": "Cliente creado exitosamente"})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        return super().form_invalid(form)


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy("ventas:cliente-list")

    def form_valid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            super().form_valid(form)
            return JsonResponse(
                {"success": True, "message": "Cliente actualizado exitosamente"}
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        return super().form_invalid(form)


def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return JsonResponse(
        {
            "id": cliente.id,
            "nombre": cliente.nombre,
            "apellido": cliente.apellido,
            "direccion": cliente.direccion,
            "email": cliente.email,
            "nit": cliente.nit,
            "activo": cliente.activo,
            "dpi": cliente.dpi,
        }
    )


def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.activo = False
    cliente.save(update_fields=["activo"])
    return redirect("ventas:cliente-list")


class FacturaListView(ListView):
    model = Factura
    template_name = "ventas_list.html"
    context_object_name = "ventas"
    paginate_by = 10

    def _lugares_filtro_qs(self):
        return Lugar.objects.filter(Q(eliminado=False) | Q(eliminado__isnull=True)).order_by(
            "nombre"
        )

    def dispatch(self, request, *args, **kwargs):
        lugares_qs = self._lugares_filtro_qs()
        first_lugar = lugares_qs.first()
        if first_lugar is None:
            return super().dispatch(request, *args, **kwargs)
        lugar_param = (request.GET.get("lugar") or "").strip()
        if lugar_param != str(first_lugar.idLugar):
            q = request.GET.copy()
            q["lugar"] = str(first_lugar.idLugar)
            q["page"] = "1"
            return HttpResponseRedirect(f"{reverse('ventas:venta-list')}?{q.urlencode()}")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clientes"] = Cliente.objects.order_by("nombre", "apellido")
        context["lugares_filtro"] = self._lugares_filtro_qs()
        first_lugar = context["lugares_filtro"].first()
        context["filtro_lugar_id"] = str(first_lugar.idLugar) if first_lugar else ""
        context["filtro_fecha_desde"] = self.request.GET.get("fecha_desde", "")
        context["filtro_fecha_hasta"] = self.request.GET.get("fecha_hasta", "")
        context["filtro_anulada"] = self.request.GET.get("anulada", "")
        context["filtro_credito"] = self.request.GET.get("credito", "")
        context["filtro_cliente"] = self.request.GET.get("cliente", "")
        return context

    def get_queryset(self):
        qs = Factura.objects.select_related("cliente", "lugar").order_by("-fechahora")
        lugar = self._lugares_filtro_qs().first()
        if lugar is None:
            return Factura.objects.none()
        qs = qs.filter(lugar=lugar)

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

        cliente_id = self.request.GET.get("cliente", "").strip()
        if cliente_id:
            qs = qs.filter(cliente_id=cliente_id)

        return qs


def _get_default_lugar():
    return Lugar.objects.filter(Q(eliminado=False) | Q(eliminado__isnull=True)).order_by(
        "nombre"
    ).first()


def _venta_productos_lugar_qs(lugar):
    return (
        ProductoLugar.objects.select_related("producto")
        .filter(lugar=lugar, existencia__gt=0)
        .filter(Q(habilitado=True) | Q(habilitado__isnull=True))
        .filter(
            Q(producto__eliminado=False) | Q(producto__eliminado__isnull=True),
            producto__habilitado=True,
        )
    )


def _validate_venta_stock(items, lugar):
    totals = {}
    for item in items:
        pid = item["producto_id"]
        totals[pid] = totals.get(pid, 0) + float(item["cantidad"])

    pl_map = {
        pl.producto_id: pl
        for pl in _venta_productos_lugar_qs(lugar).filter(producto_id__in=totals.keys())
    }

    for pid, cantidad in totals.items():
        pl = pl_map.get(pid)
        if pl is None:
            return "Uno de los productos ya no tiene existencia en el lugar seleccionado."
        existencia = float(pl.existencia or 0)
        if cantidad > existencia:
            nombre = pl.producto.nombre or f"Producto {pid}"
            return (
                f"Existencia insuficiente para '{nombre}'. "
                f"Solicitado: {cantidad:g}, disponible: {existencia:g}."
            )
    return None


def _build_catalog_product_options(lugar, limit=400):
    if lugar is None:
        return []
    options = []
    qs = _venta_productos_lugar_qs(lugar).order_by("producto__nombre")[:limit]
    for pl in qs:
        p = pl.producto
        options.append(
            {
                "producto_id": p.id,
                "codigo": p.codigo or "",
                "nombre": p.nombre or f"Producto {p.id}",
                "precio": p.precio or 0,
                "existencia": float(pl.existencia or 0),
            }
        )
    return options


def productos_autocomplete(request):
    query = request.GET.get("q", "").strip()
    lugar_id = (request.GET.get("lugar") or "").strip()
    lugar = _get_default_lugar()
    if lugar_id.isdigit():
        lugar = Lugar.objects.filter(pk=int(lugar_id)).first() or lugar
    if lugar is None:
        return JsonResponse({"results": []})

    qs = _venta_productos_lugar_qs(lugar)
    if query:
        qs = qs.filter(
            Q(producto__nombre__icontains=query) | Q(producto__codigo__icontains=query)
        )
    qs = qs.order_by("producto__nombre")[:40]
    return JsonResponse(
        {
            "results": [
                {
                    "producto_id": pl.producto_id,
                    "codigo": pl.producto.codigo or "",
                    "nombre": pl.producto.nombre or f"Producto {pl.producto_id}",
                    "precio": pl.producto.precio or 0,
                    "existencia": float(pl.existencia or 0),
                }
                for pl in qs
            ]
        }
    )


def venta_create(request):
    lugares_filtro = Lugar.objects.filter(
        Q(eliminado=False) | Q(eliminado__isnull=True)
    ).order_by("nombre")
    default_lugar = _get_default_lugar()
    current_lugar = default_lugar
    product_options = _build_catalog_product_options(current_lugar)
    initial_items_json = "[]"

    if request.method == "POST":
        form = VentaCreateForm(request.POST)
        raw_items = request.POST.get("items_json", "[]")
        initial_items_json = raw_items
        if current_lugar is None:
            messages.error(request, "No existe un Lugar configurado para registrar la venta.")
            return render(
                request,
                "ventas_form.html",
                {
                    "form": form,
                    "product_options": product_options,
                    "initial_items_json": initial_items_json,
                    "default_lugar": default_lugar,
                    "lugares_filtro": lugares_filtro,
                    "current_lugar": current_lugar,
                },
            )
        if form.is_valid():
            try:
                items = json.loads(raw_items)
            except json.JSONDecodeError:
                items = None
            if not isinstance(items, list) or len(items) == 0:
                messages.error(request, "Debe agregar al menos un producto a la venta.")
                return render(
                    request,
                    "ventas_form.html",
                    {
                        "form": form,
                        "product_options": product_options,
                        "initial_items_json": initial_items_json,
                        "default_lugar": default_lugar,
                        "lugares_filtro": lugares_filtro,
                        "current_lugar": current_lugar,
                    },
                )
            normalized = []
            for item in items:
                try:
                    pid = int(item.get("producto_id"))
                    cantidad = float(item.get("cantidad"))
                except (TypeError, ValueError):
                    messages.error(request, "Los items tienen valores inválidos.")
                    return render(
                        request,
                        "ventas_form.html",
                        {
                            "form": form,
                            "product_options": product_options,
                            "initial_items_json": initial_items_json,
                            "default_lugar": default_lugar,
                            "lugares_filtro": lugares_filtro,
                            "current_lugar": current_lugar,
                        },
                    )
                if cantidad <= 0:
                    messages.error(request, "La cantidad debe ser mayor a 0.")
                    return render(
                        request,
                        "ventas_form.html",
                        {
                            "form": form,
                            "product_options": product_options,
                            "initial_items_json": initial_items_json,
                            "default_lugar": default_lugar,
                            "lugares_filtro": lugares_filtro,
                            "current_lugar": current_lugar,
                        },
                    )
                normalized.append({"producto_id": pid, "cantidad": cantidad})

            merged = {}
            for item in normalized:
                pid = item["producto_id"]
                merged[pid] = merged.get(pid, 0) + float(item["cantidad"])
            normalized = [
                {"producto_id": pid, "cantidad": qty} for pid, qty in merged.items()
            ]

            stock_error = _validate_venta_stock(normalized, current_lugar)
            if stock_error:
                messages.error(request, stock_error)
                return render(
                    request,
                    "ventas_form.html",
                    {
                        "form": form,
                        "product_options": product_options,
                        "initial_items_json": initial_items_json,
                        "default_lugar": default_lugar,
                        "lugares_filtro": lugares_filtro,
                        "current_lugar": current_lugar,
                    },
                )

            try:
                with transaction.atomic():
                    cliente = form.cleaned_data["cliente"]
                    fecha = form.cleaned_data["fecha"]
                    fecha_dt = datetime.combine(fecha, timezone.localtime().time())
                    host = inventory_services.resolve_operation_host(request=request)
                    lugarreq, _ = LugarReq.objects.get_or_create(
                        nombre=current_lugar.nombre if current_lugar else "Lugar",
                        defaults={
                            "direccion": "",
                            "telefono": "",
                        },
                    )
                    factura = Factura.objects.create(
                        fechahora=fecha_dt,
                        usuario_id=None,
                        host=request.get_host()[:45] if request.get_host() else None,
                        anulada=False,
                        entregada=False,
                        total=0,
                        credito=False,
                        nombrefactura=(cliente.nombre if cliente else None),
                        direccionfactura=(cliente.direccion if cliente else None),
                        nitfactura=(cliente.nit if cliente else None),
                        impresa=False,
                        nofactura=str((Factura.objects.order_by("-id").first() or Factura(id=0)).id + 1),
                        refacturado=False,
                        clientesvarios=False,
                        lugar=current_lugar,
                        cliente=cliente,
                        lugarreq=lugarreq,
                    )
                    total = 0
                    for item in normalized:
                        pl = (
                            _venta_productos_lugar_qs(current_lugar)
                            .filter(producto_id=item["producto_id"])
                            .first()
                        )
                        if pl is None:
                            raise ValueError(
                                "Uno de los productos ya no tiene existencia en el lugar seleccionado."
                            )
                        producto = pl.producto
                        derivado = Derivado.objects.filter(medida=producto.medida).order_by("id").first()
                        if derivado is None:
                            raise ValueError(
                                f"El producto '{producto.nombre}' no tiene derivado asociado para venta."
                            )
                        precio = float(producto.precio or 0)
                        cantidad = float(item["cantidad"])
                        detalle = DetalleFactura.objects.create(
                            cantidad=cantidad,
                            cantidad_real=cantidad,
                            cantidad_entregada=0,
                            cantidad_entregada_real=0,
                            cantidad_devuelta=0,
                            cantidad_devuelta_real=0,
                            anulado=False,
                            devolver=False,
                            precionormal=precio,
                            precioventa=precio,
                            productolugar=pl,
                            factura=factura,
                            derivado=derivado,
                        )
                        inventory_services.registrar_salida_venta_detalle(
                            detalle,
                            nofactura=factura.nofactura or factura.id,
                            detalle_factura_id=detalle.factura_id,
                            request=request,
                            host=host,
                        )
                        total += precio * cantidad
                    factura.total = total
                    factura.save(update_fields=["total"])
            except ValueError as exc:
                messages.error(request, str(exc))
                return render(
                    request,
                    "ventas_form.html",
                    {
                        "form": form,
                        "product_options": product_options,
                        "initial_items_json": initial_items_json,
                        "default_lugar": default_lugar,
                        "lugares_filtro": lugares_filtro,
                        "current_lugar": current_lugar,
                    },
                )

            messages.success(request, "Venta creada exitosamente.")
            return redirect("ventas:venta-list")
    else:
        form = VentaCreateForm(
            initial={"fecha": timezone.localdate(), "lugar": default_lugar.pk if default_lugar else None}
        )
    return render(
        request,
        "ventas_form.html",
        {
            "form": form,
            "product_options": product_options,
            "initial_items_json": initial_items_json,
            "default_lugar": default_lugar,
            "lugares_filtro": lugares_filtro,
            "current_lugar": current_lugar,
        },
    )


def venta_detail(request, pk):
    factura = get_object_or_404(Factura.objects.select_related("cliente", "lugar"), pk=pk)
    detalles = factura.detallefactura_set.select_related("productolugar__producto").all().order_by("id")
    return JsonResponse(
        {
            "id": factura.id,
            "factura": factura.nofactura,
            "fecha": timezone.localtime(factura.fechahora).strftime("%Y-%m-%d %H:%M")
            if factura.fechahora
            else "",
            "cliente": str(factura.cliente) if factura.cliente else "—",
            "lugar": factura.lugar.nombre if factura.lugar else "—",
            "anulada": bool(factura.anulada),
            "total": float(factura.total or 0),
            "detalles": [
                {
                    "id": d.id,
                    "producto": d.productolugar.producto.nombre if d.productolugar else "—",
                    "cantidad": float(d.cantidad or 0),
                    "costo": float(d.precioventa or 0),
                    "subtotal": float((d.cantidad or 0) * (d.precioventa or 0)),
                    "anulada": bool(d.anulado),
                }
                for d in detalles
            ],
        }
    )


def venta_anular(request, pk):
    if request.method != "POST":
        return HttpResponseBadRequest("Método no permitido.")
    factura = get_object_or_404(Factura.objects.select_related("lugar"), pk=pk)
    try:
        inventory_services.anular_venta_y_revertir_stock(factura, request=request)
    except ValueError as exc:
        messages.error(request, str(exc))
    else:
        messages.success(request, f"Venta {factura.nofactura or factura.pk} anulada correctamente.")
    return redirect("ventas:venta-list")
