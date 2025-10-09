from django import forms
from .models import Categoria, Medida, Derivado, Proveedor, Producto


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

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'nombregenerico', 'descripcion', 'precio', 'habilitado', 'maximo', 'minimo', 'composicion', 'presentacion', 'es_producto', 'proveedor', 'medida', 'categoria']
        labels = {
            'codigo': 'Código',
            'nombre': 'Nombre del producto',
            'nombregenerico': 'Nombre genérico',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'habilitado': 'Habilitado',
            'maximo': 'Cantidad máxima',
            'minimo': 'Cantidad mínima',
            'composicion': 'Composición',
            'presentacion': 'Presentación',
            'proveedor': 'Proveedor',
            'medida': 'Medida',
            'categoria': 'Categoría',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el código'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del producto', 'required': 'required'}),
            'nombregenerico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre genérico'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el precio'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'maximo': forms.NumberInput(attrs={'class': 'form-control', 	'placeholder': 'Ingrese la cantidad máxima'}),
            'minimo': forms.NumberInput(attrs={'class': 'form-control', 	'placeholder': 	'Ingrese la cantidad mínima'}),
            'composicion': forms.TextInput(attrs={'class': 'form-control', 	'placeholder': 	'Ingrese la composición'}),
            'presentacion': forms.TextInput(attrs={'class': 	'form-control', 	'placeholder': 	'Ingrese la presentación'}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'medida': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter only active and non-deleted records
        from django.db.models import Q
        
        # Filter proveedores: only active and not deleted
        self.fields['proveedor'].queryset = Proveedor.objects.filter(
            Q(habilitado=True) | Q(habilitado__isnull=True),
            Q(eliminado=False) | Q(eliminado__isnull=True)
        ).order_by('nombre')
        
        # Filter medidas: only active and not deleted
        self.fields['medida'].queryset = Medida.objects.filter(
            Q(habilitado=True) | Q(habilitado__isnull=True),
            Q(eliminado=False) | Q(eliminado__isnull=True)
        ).order_by('medida')
        
        # Filter categorias: only active and not deleted
        self.fields['categoria'].queryset = Categoria.objects.filter(
            Q(habilitado=True) | Q(habilitado__isnull=True),
            Q(eliminado=False) | Q(eliminado__isnull=True)
        ).order_by('categoria')
