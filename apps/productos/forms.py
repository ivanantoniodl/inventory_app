from django import forms
from .models import Categoria, Medida, Derivado, Proveedor


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['categoria', 'habilitado']
        labels = {
            'categoria': 'Nombre de la categoría',
        }
        widgets = {
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la categoría', 'required': 'required'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }            

class MedidaForm(forms.ModelForm):
    class Meta:
        model = Medida
        fields = ['medida', 'habilitado']
        labels = {
            'medida': 'Nombre de la medida',
        }
        widgets = {
            'medida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la medida', 'required': 'required'}),            
            'habilitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }   

class DerivadoForm(forms.ModelForm):
    class Meta:
        model = Derivado
        fields = ['derivado', 'factorconversion']
        labels = {
            'derivado': 'Nombre del derivado',
            'factorconversion': 'Factor de Conversión',
        }
        widgets = {
            'derivado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el derivado', 'required': 'required'}),            
            'factorconversion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el factor de conversión', 'required': 'required'}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'direccion', 'nit', 'observaciones', 'habilitado']
        labels = {
            'nombre': 'Nombre del proveedor',
            'contacto': 'Contacto',
            'direccion': 'Dirección',
            'nit': 'NIT',
            'observaciones': 'Observaciones',
            'habilitado': 'Habilitado',
        }   
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del proveedor', 'required': 'required'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el contacto'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la dirección'}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el NIT'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese observaciones', 'rows': 3}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }