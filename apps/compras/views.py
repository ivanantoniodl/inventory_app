from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .forms import ProveedorForm
from .models import Compra
from .models import Proveedor


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
