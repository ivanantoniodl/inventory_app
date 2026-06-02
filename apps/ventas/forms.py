from django import forms
from django.db.models import Q

from apps.lugares.models import Lugar

from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "apellido", "direccion", "email", "nit", "activo", "dpi"]
        labels = {
            "nombre": "Nombre",
            "apellido": "Apellido",
            "direccion": "Dirección",
            "email": "Email",
            "nit": "NIT",
            "activo": "Activo",
            "dpi": "DPI",
        }
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingrese el nombre"}
            ),
            "apellido": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingrese el apellido"}
            ),
            "direccion": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingrese la dirección"}
            ),
            "email": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingrese el email"}
            ),
            "nit": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingrese el NIT"}
            ),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "dpi": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingrese el DPI"}
            ),
        }


class VentaCreateForm(forms.Form):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.none(),
        label="Cliente",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    lugar = forms.ModelChoiceField(
        queryset=Lugar.objects.none(),
        required=False,
        label="Lugar (opcional)",
        empty_label="Seleccionar automáticamente",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cliente"].queryset = Cliente.objects.filter(
            Q(activo=True) | Q(activo__isnull=True)
        ).order_by("nombre", "apellido")
        self.fields["lugar"].queryset = Lugar.objects.filter(
            Q(eliminado=False) | Q(eliminado__isnull=True)
        ).order_by("nombre")
