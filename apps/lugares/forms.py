from django import forms
from django.db.models import Q
from .models import Empresa, Lugar, LugarTipo


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre de la empresa',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la empresa', 'required': 'required'}),
        }


class LugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = ['empresa', 'lugar_tipo', 'nombre', 'direccion', 'telefono']
        labels = {
            'empresa': 'Empresa',
            'lugar_tipo': 'Tipo de lugar',
            'nombre': 'Nombre del lugar',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
        }
        widgets = {
            'empresa': forms.Select(attrs={'class': 'form-control'}),
            'lugar_tipo': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del lugar'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la dirección'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el teléfono'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter only active records
        self.fields['empresa'].queryset = (
            Empresa.objects.filter(Q(eliminado=False) | Q(eliminado__isnull=True))
            .order_by('nombre')
        )
        self.fields['lugar_tipo'].queryset = (
            LugarTipo.objects.filter(Q(eliminado=False) | Q(eliminado__isnull=True))
            .order_by('tipo')
        )


class LugarTipoForm(forms.ModelForm):
    class Meta:
        model = LugarTipo
        fields = ['tipo']
        labels = {
            'tipo': 'Nombre del tipo de lugar',
        }
        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del tipo de lugar', 'required': 'required'}),
        }
