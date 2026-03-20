from django import forms
from django.db.models import Q

from apps.lugares.models import Lugar

from .models import Proveedor


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nombre", "contacto", "direccion", "nit", "observaciones", "habilitado"]
        labels = {
            "nombre": "Nombre del proveedor",
            "contacto": "Contacto",
            "direccion": "Dirección",
            "nit": "NIT",
            "observaciones": "Observaciones",
            "habilitado": "Habilitado",
        }
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese el nombre del proveedor",
                    "required": "required",
                }
            ),
            "contacto": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingrese el contacto"}
            ),
            "direccion": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingrese la dirección"}
            ),
            "nit": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingrese el NIT"}
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ingrese observaciones",
                    "rows": 3,
                }
            ),
            "habilitado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CompraCreateForm(forms.Form):
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.none(),
        label="Proveedor",
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
        self.fields["proveedor"].queryset = Proveedor.objects.filter(
            Q(eliminado=False) | Q(eliminado__isnull=True)
        ).order_by("nombre")
        self.fields["lugar"].queryset = Lugar.objects.filter(
            Q(eliminado=False) | Q(eliminado__isnull=True)
        ).order_by("nombre")
