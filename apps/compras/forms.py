from django import forms

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
