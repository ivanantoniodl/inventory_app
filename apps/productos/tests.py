from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
import json

from .models import Categoria, Medida, Derivado, Proveedor, Producto, ProductoLugar, Lote
from .forms import CategoriaForm, MedidaForm, DerivadoForm, ProveedorForm, ProductoForm


class CategoriaModelTestCase(TestCase):
    """Test cases for Categoria model"""
    
    def setUp(self):
        self.categoria = Categoria.objects.create(
            categoria='Reactivos',
            habilitado=True,
            es_producto=True,
            eliminado=False
        )
    
    def test_categoria_creation(self):
        """Test Categoria model creation"""
        self.assertEqual(self.categoria.categoria, 'Reactivos')
        self.assertTrue(self.categoria.habilitado)
        self.assertTrue(self.categoria.es_producto)
        self.assertFalse(self.categoria.eliminado)
        self.assertTrue(self.categoria.id)
    
    def test_categoria_str(self):
        """Test Categoria string representation"""
        self.assertEqual(str(self.categoria), 'Reactivos')
    
    def test_categoria_str_empty_categoria(self):
        """Test Categoria string representation with empty categoria"""
        categoria_empty = Categoria.objects.create(categoria=None)
        self.assertEqual(str(categoria_empty), f"Categoría {categoria_empty.id}")


class MedidaModelTestCase(TestCase):
    """Test cases for Medida model"""
    
    def setUp(self):
        self.medida = Medida.objects.create(
            medida='Litros',
            habilitado=True,
            es_producto=True,
            eliminado=False
        )
    
    def test_medida_creation(self):
        """Test Medida model creation"""
        self.assertEqual(self.medida.medida, 'Litros')
        self.assertTrue(self.medida.habilitado)
        self.assertTrue(self.medida.es_producto)
        self.assertFalse(self.medida.eliminado)
        self.assertTrue(self.medida.id)
    
    def test_medida_str(self):
        """Test Medida string representation"""
        self.assertEqual(str(self.medida), 'Litros')
    
    def test_medida_str_empty_medida(self):
        """Test Medida string representation with empty medida"""
        medida_empty = Medida.objects.create(medida=None)
        self.assertEqual(str(medida_empty), f"Medida {medida_empty.id}")


class DerivadoModelTestCase(TestCase):
    """Test cases for Derivado model"""
    
    def setUp(self):
        self.medida = Medida.objects.create(medida='Litros')
        self.derivado = Derivado.objects.create(
            derivado='Mililitros',
            medida=self.medida,
            factorconversion=1000.0,
            eliminado=False
        )
    
    def test_derivado_creation(self):
        """Test Derivado model creation"""
        self.assertEqual(self.derivado.derivado, 'Mililitros')
        self.assertEqual(self.derivado.medida, self.medida)
        self.assertEqual(self.derivado.factorconversion, 1000.0)
        self.assertFalse(self.derivado.eliminado)
        self.assertTrue(self.derivado.id)


class ProveedorModelTestCase(TestCase):
    """Test cases for Proveedor model"""
    
    def setUp(self):
        self.proveedor = Proveedor.objects.create(
            nombre='Laboratorio Leoss',
            contacto='Juan Pérez',
            direccion='Zona 10, Guatemala',
            nit='12345678-9',
            observaciones='Proveedor confiable',
            habilitado=True,
            es_producto=True,
            saldo=0.0,
            eliminado=False
        )
    
    def test_proveedor_creation(self):
        """Test Proveedor model creation"""
        self.assertEqual(self.proveedor.nombre, 'Laboratorio Leoss')
        self.assertEqual(self.proveedor.contacto, 'Juan Pérez')
        self.assertEqual(self.proveedor.direccion, 'Zona 10, Guatemala')
        self.assertEqual(self.proveedor.nit, '12345678-9')
        self.assertEqual(self.proveedor.observaciones, 'Proveedor confiable')
        self.assertTrue(self.proveedor.habilitado)
        self.assertTrue(self.proveedor.es_producto)
        self.assertEqual(self.proveedor.saldo, 0.0)
        self.assertFalse(self.proveedor.eliminado)
        self.assertTrue(self.proveedor.id)
    
    def test_proveedor_str(self):
        """Test Proveedor string representation"""
        self.assertEqual(str(self.proveedor), 'Laboratorio Leoss')
    
    def test_proveedor_str_empty_nombre(self):
        """Test Proveedor string representation with empty nombre"""
        proveedor_empty = Proveedor.objects.create(nombre=None)
        self.assertEqual(str(proveedor_empty), f"Proveedor {proveedor_empty.id}")


class ProductoModelTestCase(TestCase):
    """Test cases for Producto model"""
    
    def setUp(self):
        self.categoria = Categoria.objects.create(categoria='Reactivos')
        self.medida = Medida.objects.create(medida='Litros')
        self.proveedor = Proveedor.objects.create(nombre='Laboratorio Leoss')
        
        self.producto = Producto.objects.create(
            codigo='PROD001',
            nombre='Alcohol Etílico',
            nombregenerico='Etanol',
            descripcion='Alcohol para desinfección',
            precio=25.50,
            habilitado=True,
            maximo=100,
            minimo=10,
            composicion='Etanol 96%',
            presentacion='Frasco 500ml',
            es_producto=True,
            proveedor=self.proveedor,
            medida=self.medida,
            categoria=self.categoria,
            eliminado=False
        )
    
    def test_producto_creation(self):
        """Test Producto model creation"""
        self.assertEqual(self.producto.codigo, 'PROD001')
        self.assertEqual(self.producto.nombre, 'Alcohol Etílico')
        self.assertEqual(self.producto.nombregenerico, 'Etanol')
        self.assertEqual(self.producto.descripcion, 'Alcohol para desinfección')
        self.assertEqual(self.producto.precio, 25.50)
        self.assertTrue(self.producto.habilitado)
        self.assertEqual(self.producto.maximo, 100)
        self.assertEqual(self.producto.minimo, 10)
        self.assertEqual(self.producto.composicion, 'Etanol 96%')
        self.assertEqual(self.producto.presentacion, 'Frasco 500ml')
        self.assertTrue(self.producto.es_producto)
        self.assertEqual(self.producto.proveedor, self.proveedor)
        self.assertEqual(self.producto.medida, self.medida)
        self.assertEqual(self.producto.categoria, self.categoria)
        self.assertFalse(self.producto.eliminado)
        self.assertTrue(self.producto.id)


class ProductoLugarModelTestCase(TestCase):
    """Test cases for ProductoLugar model"""
    
    def setUp(self):
        self.categoria = Categoria.objects.create(categoria='Reactivos')
        self.medida = Medida.objects.create(medida='Litros')
        self.producto = Producto.objects.create(
            nombre='Test Producto',
            medida=self.medida,
            categoria=self.categoria
        )
        self.producto_lugar = ProductoLugar.objects.create(
            existencia=50.0,
            habilitado=True,
            producto=self.producto
        )
    
    def test_producto_lugar_creation(self):
        """Test ProductoLugar model creation"""
        self.assertEqual(self.producto_lugar.existencia, 50.0)
        self.assertTrue(self.producto_lugar.habilitado)
        self.assertEqual(self.producto_lugar.producto, self.producto)
        self.assertTrue(self.producto_lugar.id)


class LoteModelTestCase(TestCase):
    """Test cases for Lote model"""
    
    def setUp(self):
        self.categoria = Categoria.objects.create(categoria='Reactivos')
        self.medida = Medida.objects.create(medida='Litros')
        self.producto = Producto.objects.create(
            nombre='Test Producto',
            medida=self.medida,
            categoria=self.categoria
        )
        self.producto_lugar = ProductoLugar.objects.create(
            producto=self.producto,
            existencia=50.0
        )
        self.lote = Lote.objects.create(
            existencia=25.0,
            costo=20.0,
            costodescuento=18.0,
            fechaingreso=date.today(),
            terminado=5.0,
            lotetotal=30.0,
            fecha_vencimiento=date(2024, 12, 31),
            productolugar=self.producto_lugar
        )
    
    def test_lote_creation(self):
        """Test Lote model creation"""
        self.assertEqual(self.lote.existencia, 25.0)
        self.assertEqual(self.lote.costo, 20.0)
        self.assertEqual(self.lote.costodescuento, 18.0)
        self.assertEqual(self.lote.fechaingreso, date.today())
        self.assertEqual(self.lote.terminado, 5.0)
        self.assertEqual(self.lote.lotetotal, 30.0)
        self.assertEqual(self.lote.fecha_vencimiento, date(2024, 12, 31))
        self.assertEqual(self.lote.productolugar, self.producto_lugar)
        self.assertTrue(self.lote.id)


class CategoriaFormTestCase(TestCase):
    """Test cases for CategoriaForm"""
    
    def test_categoria_form_valid_data(self):
        """Test CategoriaForm with valid data"""
        form_data = {
            'categoria': 'Nueva Categoría',
            'habilitado': True
        }
        form = CategoriaForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_categoria_form_empty_data(self):
        """Test CategoriaForm with empty data"""
        form = CategoriaForm(data={})
        self.assertTrue(form.is_valid())  # categoria is not required in model
    
    def test_categoria_form_widget_attrs(self):
        """Test CategoriaForm widget attributes"""
        form = CategoriaForm()
        categoria_widget = form.fields['categoria'].widget
        self.assertIn('form-control', categoria_widget.attrs['class'])
        self.assertIn('Ingrese la categoría', categoria_widget.attrs['placeholder'])


class MedidaFormTestCase(TestCase):
    """Test cases for MedidaForm"""
    
    def test_medida_form_valid_data(self):
        """Test MedidaForm with valid data"""
        form_data = {
            'medida': 'Nueva Medida',
            'habilitado': True
        }
        form = MedidaForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_medida_form_widget_attrs(self):
        """Test MedidaForm widget attributes"""
        form = MedidaForm()
        medida_widget = form.fields['medida'].widget
        self.assertIn('form-control', medida_widget.attrs['class'])
        self.assertIn('Ingrese la medida', medida_widget.attrs['placeholder'])


class DerivadoFormTestCase(TestCase):
    """Test cases for DerivadoForm"""
    
    def setUp(self):
        self.medida = Medida.objects.create(medida='Litros')
    
    def test_derivado_form_valid_data(self):
        """Test DerivadoForm with valid data"""
        form_data = {
            'derivado': 'Mililitros',
            'factorconversion': 1000.0
        }
        form = DerivadoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_derivado_form_widget_attrs(self):
        """Test DerivadoForm widget attributes"""
        form = DerivadoForm()
        derivado_widget = form.fields['derivado'].widget
        factor_widget = form.fields['factorconversion'].widget
        self.assertIn('form-control', derivado_widget.attrs['class'])
        self.assertIn('form-control', factor_widget.attrs['class'])


class ProveedorFormTestCase(TestCase):
    """Test cases for ProveedorForm"""
    
    def test_proveedor_form_valid_data(self):
        """Test ProveedorForm with valid data"""
        form_data = {
            'nombre': 'Nuevo Proveedor',
            'contacto': 'Juan Pérez',
            'direccion': 'Zona 10',
            'nit': '12345678-9',
            'observaciones': 'Proveedor confiable',
            'habilitado': True
        }
        form = ProveedorForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_proveedor_form_widget_attrs(self):
        """Test ProveedorForm widget attributes"""
        form = ProveedorForm()
        nombre_widget = form.fields['nombre'].widget
        self.assertIn('form-control', nombre_widget.attrs['class'])
        self.assertIn('Ingrese el nombre del proveedor', nombre_widget.attrs['placeholder'])


class ProductoFormTestCase(TestCase):
    """Test cases for ProductoForm"""
    
    def setUp(self):
        self.categoria = Categoria.objects.create(categoria='Test Categoría')
        self.medida = Medida.objects.create(medida='Test Medida')
        self.proveedor = Proveedor.objects.create(nombre='Test Proveedor')
    
    def test_producto_form_valid_data(self):
        """Test ProductoForm with valid data"""
        form_data = {
            'codigo': 'PROD001',
            'nombre': 'Test Producto',
            'nombregenerico': 'Test Genérico',
            'descripcion': 'Test Descripción',
            'precio': 25.50,
            'habilitado': True,
            'maximo': 100,
            'minimo': 10,
            'composicion': 'Test Composición',
            'presentacion': 'Test Presentación',
            'es_producto': True,
            'proveedor': self.proveedor.id,
            'medida': self.medida.id,
            'categoria': self.categoria.id
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_producto_form_missing_required_fields(self):
        """Test ProductoForm with missing required fields"""
        form_data = {
            'medida': self.medida.id  # Only required field
        }
        form = ProductoForm(data=form_data)
        self.assertTrue(form.is_valid())  # medida is the only required field
    
    def test_producto_form_queryset_filtering(self):
        """Test ProductoForm queryset filtering"""
        # Create inactive/deleted records
        Categoria.objects.create(categoria='Inactive Cat', habilitado=False)
        Categoria.objects.create(categoria='Deleted Cat', eliminado=True)
        
        Medida.objects.create(medida='Inactive Med', habilitado=False)
        Medida.objects.create(medida='Deleted Med', eliminado=True)
        
        Proveedor.objects.create(nombre='Inactive Prov', habilitado=False)
        Proveedor.objects.create(nombre='Deleted Prov', eliminado=True)
        
        form = ProductoForm()
        
        # Should only include active, non-deleted records
        self.assertEqual(form.fields['categoria'].queryset.count(), 1)  # Only 'Test Categoría'
        self.assertEqual(form.fields['medida'].queryset.count(), 1)     # Only 'Test Medida'
        self.assertEqual(form.fields['proveedor'].queryset.count(), 1)  # Only 'Test Proveedor'


class CategoriaViewsTestCase(TestCase):
    """Test cases for Categoria views"""
    
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(
            categoria='Test Categoría',
            habilitado=True,
            es_producto=True,
            eliminado=False
        )
    
    def test_categoria_list_view(self):
        """Test CategoriaListView"""
        response = self.client.get(reverse('productos:categoria-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Categoría')
        self.assertIn('form', response.context)
    
    def test_categoria_create_view_get(self):
        """Test CategoriaCreateView GET request"""
        response = self.client.get(reverse('productos:categoria-create'))
        self.assertEqual(response.status_code, 200)
    
    def test_categoria_create_view_post(self):
        """Test CategoriaCreateView POST request"""
        data = {'categoria': 'Nueva Categoría'}
        response = self.client.post(reverse('productos:categoria-create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertEqual(Categoria.objects.count(), 2)
        new_categoria = Categoria.objects.get(categoria='Nueva Categoría')
        self.assertTrue(new_categoria.habilitado)
        self.assertTrue(new_categoria.es_producto)
        self.assertFalse(new_categoria.eliminado)
    
    def test_categoria_create_view_ajax(self):
        """Test CategoriaCreateView AJAX request"""
        data = {'categoria': 'Categoría AJAX'}
        response = self.client.post(
            reverse('productos:categoria-create'), 
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Categoría creada exitosamente')
    
    def test_categoria_update_view_get(self):
        """Test CategoriaUpdateView GET request"""
        response = self.client.get(reverse('productos:categoria-update', kwargs={'pk': self.categoria.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Categoría')
    
    def test_categoria_update_view_post(self):
        """Test CategoriaUpdateView POST request"""
        data = {'categoria': 'Categoría Actualizada'}
        response = self.client.post(
            reverse('productos:categoria-update', kwargs={'pk': self.categoria.id}), 
            data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after update
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.categoria, 'Categoría Actualizada')
    
    def test_categoria_detail_view(self):
        """Test categoria_detail view"""
        response = self.client.get(reverse('productos:categoria-detail', kwargs={'pk': self.categoria.id}))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['id'], self.categoria.id)
        self.assertEqual(response_data['categoria'], 'Test Categoría')
    
    def test_categoria_delete_view(self):
        """Test categoria_delete view (soft delete)"""
        response = self.client.get(reverse('productos:categoria-delete', kwargs={'pk': self.categoria.id}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.categoria.refresh_from_db()
        self.assertTrue(self.categoria.eliminado)
        self.assertIsNotNone(self.categoria.eliminado_ts)


class MedidaViewsTestCase(TestCase):
    """Test cases for Medida views"""
    
    def setUp(self):
        self.client = Client()
        self.medida = Medida.objects.create(
            medida='Test Medida',
            habilitado=True,
            es_producto=True,
            eliminado=False
        )
    
    def test_medida_list_view(self):
        """Test MedidaListView"""
        response = self.client.get(reverse('productos:medida-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Medida')
        self.assertIn('form', response.context)
    
    def test_medida_create_view_post(self):
        """Test MedidaCreateView POST request"""
        data = {'medida': 'Nueva Medida'}
        response = self.client.post(reverse('productos:medida-create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertEqual(Medida.objects.count(), 2)
        new_medida = Medida.objects.get(medida='Nueva Medida')
        self.assertTrue(new_medida.habilitado)
        self.assertTrue(new_medida.es_producto)
        self.assertFalse(new_medida.eliminado)
    
    def test_medida_create_view_ajax(self):
        """Test MedidaCreateView AJAX request"""
        data = {'medida': 'Medida AJAX'}
        response = self.client.post(
            reverse('productos:medida-create'), 
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Medida creada exitosamente')
    
    def test_medida_detail_view(self):
        """Test medida_detail view"""
        response = self.client.get(reverse('productos:medida-detail', kwargs={'pk': self.medida.id}))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['id'], self.medida.id)
        self.assertEqual(response_data['medida'], 'Test Medida')
    
    def test_medida_delete_view(self):
        """Test medida_delete view (soft delete)"""
        response = self.client.get(reverse('productos:medida-delete', kwargs={'pk': self.medida.id}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.medida.refresh_from_db()
        self.assertTrue(self.medida.eliminado)
        self.assertIsNotNone(self.medida.eliminado_ts)


class DerivadoViewsTestCase(TestCase):
    """Test cases for Derivado views"""
    
    def setUp(self):
        self.client = Client()
        self.medida = Medida.objects.create(medida='Test Medida')
        self.derivado = Derivado.objects.create(
            derivado='Test Derivado',
            medida=self.medida,
            factorconversion=1000.0
        )
    
    def test_get_derivados_view(self):
        """Test get_derivados view"""
        response = self.client.get(reverse('productos:medida-derivados', kwargs={'pk': self.medida.id}))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['medida'], 'Test Medida')
        self.assertEqual(len(response_data['derivados']), 1)
        self.assertEqual(response_data['derivados'][0]['derivado'], 'Test Derivado')
    
    def test_derivado_create_view_post(self):
        """Test DerivadoCreateView POST request"""
        data = {
            'derivado': 'Nuevo Derivado',
            'factorconversion': 500.0
        }
        response = self.client.post(
            reverse('productos:crear-derivado', kwargs={'pk': self.medida.id}), 
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(Derivado.objects.count(), 2)
    
    def test_derivados_delete_view(self):
        """Test DerivadosDeleteView"""
        response = self.client.post(
            reverse('productos:delete-derivado', kwargs={'pk': self.derivado.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertFalse(Derivado.objects.filter(id=self.derivado.id).exists())


class ProveedorViewsTestCase(TestCase):
    """Test cases for Proveedor views"""
    
    def setUp(self):
        self.client = Client()
        self.proveedor = Proveedor.objects.create(
            nombre='Test Proveedor',
            contacto='Juan Pérez',
            habilitado=True,
            es_producto=True,
            saldo=0.0,
            eliminado=False
        )
    
    def test_proveedor_list_view(self):
        """Test ProveedorListView"""
        response = self.client.get(reverse('productos:proveedor-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Proveedor')
        self.assertIn('form', response.context)
    
    def test_proveedor_create_view_post(self):
        """Test ProveedorCreateView POST request"""
        data = {
            'nombre': 'Nuevo Proveedor',
            'contacto': 'María García',
            'direccion': 'Zona 10',
            'nit': '87654321-0'
        }
        response = self.client.post(reverse('productos:proveedor-create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertEqual(Proveedor.objects.count(), 2)
        new_proveedor = Proveedor.objects.get(nombre='Nuevo Proveedor')
        self.assertTrue(new_proveedor.habilitado)
        self.assertTrue(new_proveedor.es_producto)
        self.assertEqual(new_proveedor.saldo, 0.0)
        self.assertFalse(new_proveedor.eliminado)
    
    def test_proveedor_create_view_ajax(self):
        """Test ProveedorCreateView AJAX request"""
        data = {'nombre': 'Proveedor AJAX'}
        response = self.client.post(
            reverse('productos:proveedor-create'), 
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Proveedor creado exitosamente')
    
    def test_proveedor_detail_view(self):
        """Test proveedor_detail view"""
        response = self.client.get(reverse('productos:proveedor-detail', kwargs={'pk': self.proveedor.id}))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['id'], self.proveedor.id)
        self.assertEqual(response_data['nombre'], 'Test Proveedor')
    
    def test_proveedor_delete_view(self):
        """Test proveedor_delete view (soft delete)"""
        response = self.client.get(reverse('productos:proveedor-delete', kwargs={'pk': self.proveedor.id}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.proveedor.refresh_from_db()
        self.assertTrue(self.proveedor.eliminado)
        self.assertIsNotNone(self.proveedor.eliminado_ts)


class ProductoViewsTestCase(TestCase):
    """Test cases for Producto views"""
    
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(categoria='Test Categoría')
        self.medida = Medida.objects.create(medida='Test Medida')
        self.proveedor = Proveedor.objects.create(nombre='Test Proveedor')
        
        self.producto = Producto.objects.create(
            codigo='PROD001',
            nombre='Test Producto',
            medida=self.medida,
            categoria=self.categoria,
            proveedor=self.proveedor,
            habilitado=True,
            es_producto=True,
            eliminado=False
        )
        
        # Create ProductoLugar and Lote for testing
        self.producto_lugar = ProductoLugar.objects.create(
            producto=self.producto,
            existencia=50.0
        )
        
        self.lote = Lote.objects.create(
            existencia=25.0,
            costo=20.0,
            productolugar=self.producto_lugar,
            fechaingreso=date.today()
        )
    
    def test_producto_list_view(self):
        """Test ProductoListView"""
        response = self.client.get(reverse('productos:producto-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Producto')
        self.assertIn('form', response.context)
    
    def test_producto_create_view_post(self):
        """Test ProductoCreateView POST request"""
        data = {
            'codigo': 'PROD002',
            'nombre': 'Nuevo Producto',
            'medida': self.medida.id,
            'categoria': self.categoria.id,
            'proveedor': self.proveedor.id
        }
        response = self.client.post(reverse('productos:producto-create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertEqual(Producto.objects.count(), 2)
        new_producto = Producto.objects.get(nombre='Nuevo Producto')
        self.assertTrue(new_producto.habilitado)
        self.assertTrue(new_producto.es_producto)
        self.assertFalse(new_producto.eliminado)
    
    def test_producto_create_view_ajax(self):
        """Test ProductoCreateView AJAX request"""
        data = {
            'nombre': 'Producto AJAX',
            'medida': self.medida.id
        }
        response = self.client.post(
            reverse('productos:producto-create'), 
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Producto creado exitosamente')
    
    def test_producto_detail_view(self):
        """Test producto_detail view"""
        response = self.client.get(reverse('productos:producto-detail', kwargs={'pk': self.producto.id}))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['id'], self.producto.id)
        self.assertEqual(response_data['nombre'], 'Test Producto')
    
    def test_producto_lotes_view(self):
        """Test producto_lotes view"""
        response = self.client.get(reverse('productos:producto-lotes', kwargs={'pk': self.producto.id}))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['producto'], 'Test Producto')
        self.assertEqual(len(response_data['lotes']), 1)
        self.assertEqual(response_data['lotes'][0]['existencia'], 25.0)
    
    def test_producto_delete_view(self):
        """Test producto_delete view (soft delete)"""
        response = self.client.get(reverse('productos:producto-delete', kwargs={'pk': self.producto.id}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.producto.refresh_from_db()
        self.assertTrue(self.producto.eliminado)
        self.assertIsNotNone(self.producto.eliminado_ts)


class ProductosURLsTestCase(TestCase):
    """Test cases for Productos URL routing"""
    
    def setUp(self):
        self.categoria = Categoria.objects.create(categoria='Test Categoría')
        self.medida = Medida.objects.create(medida='Test Medida')
        self.proveedor = Proveedor.objects.create(nombre='Test Proveedor')
        self.producto = Producto.objects.create(
            nombre='Test Producto',
            medida=self.medida
        )
        self.derivado = Derivado.objects.create(
            derivado='Test Derivado',
            medida=self.medida
        )
    
    def test_categoria_urls(self):
        """Test Categoria URL patterns"""
        response = self.client.get(reverse('productos:categoria-list'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('productos:categoria-create'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('productos:categoria-update', kwargs={'pk': self.categoria.id}))
        self.assertEqual(response.status_code, 200)
    
    def test_medida_urls(self):
        """Test Medida URL patterns"""
        response = self.client.get(reverse('productos:medida-list'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('productos:medida-create'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('productos:medida-update', kwargs={'pk': self.medida.id}))
        self.assertEqual(response.status_code, 200)
    
    def test_producto_urls(self):
        """Test Producto URL patterns"""
        response = self.client.get(reverse('productos:producto-list'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('productos:producto-create'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('productos:producto-update', kwargs={'pk': self.producto.id}))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('productos:producto-lotes', kwargs={'pk': self.producto.id}))
        self.assertEqual(response.status_code, 200)


class ProductosPaginationTestCase(TestCase):
    """Test cases for pagination in Productos views"""
    
    def setUp(self):
        self.client = Client()
        
        # Create multiple records for pagination testing
        for i in range(15):
            Categoria.objects.create(categoria=f'Categoría {i+1}')
            Medida.objects.create(medida=f'Medida {i+1}')
            Proveedor.objects.create(nombre=f'Proveedor {i+1}')
    
    def test_categoria_pagination(self):
        """Test Categoria pagination"""
        response = self.client.get(reverse('productos:categoria-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['categorias']), 10)  # First page
    
    def test_categoria_pagination_second_page(self):
        """Test Categoria pagination second page"""
        response = self.client.get(reverse('productos:categoria-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['categorias']), 5)  # Second page (15 total - 10 first page)
    
    def test_medida_pagination(self):
        """Test Medida pagination"""
        response = self.client.get(reverse('productos:medida-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['medidas']), 10)  # First page
    
    def test_medida_pagination_second_page(self):
        """Test Medida pagination second page"""
        response = self.client.get(reverse('productos:medida-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['medidas']), 5)  # Second page (15 total - 10 first page)
    
    def test_proveedor_pagination(self):
        """Test Proveedor pagination"""
        response = self.client.get(reverse('productos:proveedor-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['proveedores']), 10)  # First page
    
    def test_proveedor_pagination_second_page(self):
        """Test Proveedor pagination second page"""
        response = self.client.get(reverse('productos:proveedor-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['proveedores']), 5)  # Second page (15 total - 10 first page)