from django import forms
from .models import Categoria, Medida, Derivado


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['categoria', 'habilitado']
        widgets = {
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la categoría', 'required': 'required'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }            

class MedidaForm(forms.ModelForm):
    class Meta:
        model = Medida
        fields = ['medida', 'habilitado']
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