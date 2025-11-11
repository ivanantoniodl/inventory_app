from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User
import json

from .models import Empresa, Lugar, LugarTipo
from .forms import EmpresaForm, LugarForm


class LugarTipoModelTestCase(TestCase):
    """Test cases for LugarTipo model"""
    
    def setUp(self):
        self.lugar_tipo = LugarTipo.objects.create(tipo='Laboratorio')
    
    def test_lugar_tipo_creation(self):
        """Test LugarTipo model creation"""
        self.assertEqual(self.lugar_tipo.tipo, 'Laboratorio')
        self.assertTrue(self.lugar_tipo.idLugarTipo)
    
    def test_lugar_tipo_str(self):
        """Test LugarTipo string representation"""
        self.assertEqual(str(self.lugar_tipo), 'Laboratorio')
    
    def test_lugar_tipo_meta(self):
        """Test LugarTipo meta configuration"""
        self.assertEqual(LugarTipo._meta.verbose_name, 'Tipo de Lugar')
        self.assertEqual(LugarTipo._meta.verbose_name_plural, 'Tipos de Lugar')
        self.assertEqual(LugarTipo._meta.db_table, 'LugarTipo')


class EmpresaModelTestCase(TestCase):
    """Test cases for Empresa model"""
    
    def setUp(self):
        self.empresa = Empresa.objects.create(nombre='Laboratorio Leoss')
    
    def test_empresa_creation(self):
        """Test Empresa model creation"""
        self.assertEqual(self.empresa.nombre, 'Laboratorio Leoss')
        self.assertTrue(self.empresa.idEmpresa)
    
    def test_empresa_str(self):
        """Test Empresa string representation"""
        self.assertEqual(str(self.empresa), 'Laboratorio Leoss')
    
    def test_empresa_str_empty_nombre(self):
        """Test Empresa string representation with empty nombre"""
        empresa_empty = Empresa.objects.create(nombre=None)
        self.assertEqual(str(empresa_empty), f"Empresa {empresa_empty.idEmpresa}")
    
    def test_empresa_meta(self):
        """Test Empresa meta configuration"""
        self.assertEqual(Empresa._meta.verbose_name, 'Empresa')
        self.assertEqual(Empresa._meta.verbose_name_plural, 'Empresas')
        self.assertEqual(Empresa._meta.db_table, 'Empresa')


class LugarModelTestCase(TestCase):
    """Test cases for Lugar model"""
    
    def setUp(self):
        self.empresa = Empresa.objects.create(nombre='Laboratorio Leoss')
        self.lugar_tipo = LugarTipo.objects.create(tipo='Laboratorio')
        self.lugar = Lugar.objects.create(
            empresa=self.empresa,
            lugar_tipo=self.lugar_tipo,
            nombre='Sede Central',
            direccion='Zona 10, Guatemala',
            telefono='50212345',
            num_placa='ABC123'
        )
    
    def test_lugar_creation(self):
        """Test Lugar model creation"""
        self.assertEqual(self.lugar.nombre, 'Sede Central')
        self.assertEqual(self.lugar.empresa, self.empresa)
        self.assertEqual(self.lugar.lugar_tipo, self.lugar_tipo)
        self.assertEqual(self.lugar.direccion, 'Zona 10, Guatemala')
        self.assertEqual(self.lugar.telefono, '50212345')
        self.assertEqual(self.lugar.num_placa, 'ABC123')
        self.assertTrue(self.lugar.idLugar)
    
    def test_lugar_str(self):
        """Test Lugar string representation"""
        self.assertEqual(str(self.lugar), 'Sede Central')
    
    def test_lugar_str_empty_nombre(self):
        """Test Lugar string representation with empty nombre"""
        lugar_empty = Lugar.objects.create(
            empresa=self.empresa,
            lugar_tipo=self.lugar_tipo
        )
        self.assertEqual(str(lugar_empty), f"Lugar {lugar_empty.idLugar}")
    
    def test_lugar_meta(self):
        """Test Lugar meta configuration"""
        self.assertEqual(Lugar._meta.verbose_name, 'Lugar')
        self.assertEqual(Lugar._meta.verbose_name_plural, 'Lugares')
        self.assertEqual(Lugar._meta.db_table, 'Lugar')
    
    def test_lugar_relationships(self):
        """Test Lugar foreign key relationships"""
        self.assertEqual(self.lugar.empresa.nombre, 'Laboratorio Leoss')
        self.assertEqual(self.lugar.lugar_tipo.tipo, 'Laboratorio')
        
        # Test reverse relationships
        self.assertIn(self.lugar, self.empresa.lugares.all())
        self.assertIn(self.lugar, self.lugar_tipo.lugares.all())


class EmpresaFormTestCase(TestCase):
    """Test cases for EmpresaForm"""
    
    def test_empresa_form_valid_data(self):
        """Test EmpresaForm with valid data"""
        form_data = {'nombre': 'Nueva Empresa'}
        form = EmpresaForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_empresa_form_empty_data(self):
        """Test EmpresaForm with empty data"""
        form = EmpresaForm(data={})
        self.assertTrue(form.is_valid())  # nombre is not required
    
    def test_empresa_form_widget_attrs(self):
        """Test EmpresaForm widget attributes"""
        form = EmpresaForm()
        nombre_widget = form.fields['nombre'].widget
        self.assertIn('form-control', nombre_widget.attrs['class'])
        self.assertIn('Ingrese el nombre de la empresa', nombre_widget.attrs['placeholder'])


class LugarFormTestCase(TestCase):
    """Test cases for LugarForm"""
    
    def setUp(self):
        self.empresa = Empresa.objects.create(nombre='Test Empresa')
        self.lugar_tipo = LugarTipo.objects.create(tipo='Test Tipo')
    
    def test_lugar_form_valid_data(self):
        """Test LugarForm with valid data"""
        form_data = {
            'empresa': self.empresa.idEmpresa,
            'lugar_tipo': self.lugar_tipo.idLugarTipo,
            'nombre': 'Test Lugar',
            'direccion': 'Test Dirección',
            'telefono': '123456789',
            'num_placa': 'TEST123'
        }
        form = LugarForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_lugar_form_missing_required_fields(self):
        """Test LugarForm with missing required fields"""
        form_data = {}
        form = LugarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('empresa', form.errors)
        self.assertIn('lugar_tipo', form.errors)
    
    def test_lugar_form_widget_attrs(self):
        """Test LugarForm widget attributes"""
        form = LugarForm()
        for field_name in ['empresa', 'lugar_tipo']:
            self.assertIn('form-control', form.fields[field_name].widget.attrs['class'])
    
    def test_lugar_form_queryset_ordering(self):
        """Test LugarForm queryset ordering"""
        Empresa.objects.create(nombre='B Empresa')
        Empresa.objects.create(nombre='A Empresa')
        
        form = LugarForm()
        empresas = list(form.fields['empresa'].queryset)
        self.assertEqual(empresas[0].nombre, 'A Empresa')
        self.assertEqual(empresas[1].nombre, 'B Empresa')


class EmpresaViewsTestCase(TestCase):
    """Test cases for Empresa views"""
    
    def setUp(self):
        self.client = Client()
        self.empresa = Empresa.objects.create(nombre='Test Empresa')
    
    def test_empresa_list_view(self):
        """Test EmpresaListView"""
        response = self.client.get(reverse('lugares:empresa-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Empresa')
        self.assertIn('form', response.context)
    
    def test_empresa_create_view_get(self):
        """Test EmpresaCreateView GET request"""
        response = self.client.get(reverse('lugares:empresa-create'))
        self.assertEqual(response.status_code, 200)
    
    def test_empresa_create_view_post(self):
        """Test EmpresaCreateView POST request"""
        data = {'nombre': 'Nueva Empresa'}
        response = self.client.post(reverse('lugares:empresa-create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertEqual(Empresa.objects.count(), 2)
        self.assertTrue(Empresa.objects.filter(nombre='Nueva Empresa').exists())
    
    def test_empresa_create_view_ajax(self):
        """Test EmpresaCreateView AJAX request"""
        data = {'nombre': 'Empresa AJAX'}
        response = self.client.post(
            reverse('lugares:empresa-create'), 
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Empresa creada exitosamente')
    
    def test_empresa_update_view_get(self):
        """Test EmpresaUpdateView GET request"""
        response = self.client.get(reverse('lugares:empresa-update', kwargs={'pk': self.empresa.idEmpresa}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Empresa')
    
    def test_empresa_update_view_post(self):
        """Test EmpresaUpdateView POST request"""
        data = {'nombre': 'Empresa Actualizada'}
        response = self.client.post(
            reverse('lugares:empresa-update', kwargs={'pk': self.empresa.idEmpresa}), 
            data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after update
        self.empresa.refresh_from_db()
        self.assertEqual(self.empresa.nombre, 'Empresa Actualizada')
    
    def test_empresa_detail_view(self):
        """Test empresa_detail view"""
        response = self.client.get(reverse('lugares:empresa-detail', kwargs={'pk': self.empresa.idEmpresa}))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['id'], self.empresa.idEmpresa)
        self.assertEqual(response_data['nombre'], 'Test Empresa')
    
    def test_empresa_delete_view(self):
        """Test empresa_delete view"""
        response = self.client.get(reverse('lugares:empresa-delete', kwargs={'pk': self.empresa.idEmpresa}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Empresa.objects.filter(idEmpresa=self.empresa.idEmpresa).exists())


class LugarViewsTestCase(TestCase):
    """Test cases for Lugar views"""
    
    def setUp(self):
        self.client = Client()
        self.empresa = Empresa.objects.create(nombre='Test Empresa')
        self.lugar_tipo = LugarTipo.objects.create(tipo='Laboratorio')
        self.lugar = Lugar.objects.create(
            empresa=self.empresa,
            lugar_tipo=self.lugar_tipo,
            nombre='Test Lugar',
            direccion='Test Dirección',
            telefono='123456789',
            num_placa='TEST123'
        )
    
    def test_lugar_list_view(self):
        """Test LugarListView"""
        response = self.client.get(reverse('lugares:lugar-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Lugar')
        self.assertIn('form', response.context)
    
    def test_lugar_create_view_get(self):
        """Test LugarCreateView GET request"""
        response = self.client.get(reverse('lugares:lugar-create'))
        self.assertEqual(response.status_code, 200)
    
    def test_lugar_create_view_post(self):
        """Test LugarCreateView POST request"""
        data = {
            'empresa': self.empresa.idEmpresa,
            'lugar_tipo': self.lugar_tipo.idLugarTipo,
            'nombre': 'Nuevo Lugar',
            'direccion': 'Nueva Dirección',
            'telefono': '987654321',
            'num_placa': 'NEW123'
        }
        response = self.client.post(reverse('lugares:lugar-create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertEqual(Lugar.objects.count(), 2)
        self.assertTrue(Lugar.objects.filter(nombre='Nuevo Lugar').exists())
    
    def test_lugar_create_view_ajax(self):
        """Test LugarCreateView AJAX request"""
        data = {
            'empresa': self.empresa.idEmpresa,
            'lugar_tipo': self.lugar_tipo.idLugarTipo,
            'nombre': 'Lugar AJAX'
        }
        response = self.client.post(
            reverse('lugares:lugar-create'), 
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Lugar creado exitosamente')
    
    def test_lugar_create_view_invalid_data_ajax(self):
        """Test LugarCreateView AJAX request with invalid data"""
        data = {}  # Missing required fields
        response = self.client.post(
            reverse('lugares:lugar-create'), 
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertIn('errors', response_data)
    
    def test_lugar_update_view_get(self):
        """Test LugarUpdateView GET request"""
        response = self.client.get(reverse('lugares:lugar-update', kwargs={'pk': self.lugar.idLugar}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Lugar')
    
    def test_lugar_update_view_post(self):
        """Test LugarUpdateView POST request"""
        data = {
            'empresa': self.empresa.idEmpresa,
            'lugar_tipo': self.lugar_tipo.idLugarTipo,
            'nombre': 'Lugar Actualizado',
            'direccion': 'Dirección Actualizada',
            'telefono': '111111111',
            'num_placa': 'UPD123'
        }
        response = self.client.post(
            reverse('lugares:lugar-update', kwargs={'pk': self.lugar.idLugar}), 
            data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after update
        self.lugar.refresh_from_db()
        self.assertEqual(self.lugar.nombre, 'Lugar Actualizado')
    
    def test_lugar_detail_view(self):
        """Test lugar_detail view"""
        response = self.client.get(reverse('lugares:lugar-detail', kwargs={'pk': self.lugar.idLugar}))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['id'], self.lugar.idLugar)
        self.assertEqual(response_data['nombre'], 'Test Lugar')
        self.assertEqual(response_data['empresa'], 'Test Empresa')
        self.assertEqual(response_data['lugar_tipo'], 'Laboratorio')
    
    def test_lugar_delete_view(self):
        """Test lugar_delete view"""
        response = self.client.get(reverse('lugares:lugar-delete', kwargs={'pk': self.lugar.idLugar}))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Lugar.objects.filter(idLugar=self.lugar.idLugar).exists())


class LugaresURLsTestCase(TestCase):
    """Test cases for Lugares URL routing"""
    
    def test_empresa_urls(self):
        """Test Empresa URL patterns"""
        empresa = Empresa.objects.create(nombre='Test Empresa')
        
        # Test list URL
        response = self.client.get(reverse('lugares:empresa-list'))
        self.assertEqual(response.status_code, 200)
        
        # Test create URL
        response = self.client.get(reverse('lugares:empresa-create'))
        self.assertEqual(response.status_code, 200)
        
        # Test update URL
        response = self.client.get(reverse('lugares:empresa-update', kwargs={'pk': empresa.idEmpresa}))
        self.assertEqual(response.status_code, 200)
        
        # Test detail URL
        response = self.client.get(reverse('lugares:empresa-detail', kwargs={'pk': empresa.idEmpresa}))
        self.assertEqual(response.status_code, 200)
    
    def test_lugar_urls(self):
        """Test Lugar URL patterns"""
        empresa = Empresa.objects.create(nombre='Test Empresa')
        lugar_tipo = LugarTipo.objects.create(tipo='Laboratorio')
        lugar = Lugar.objects.create(
            empresa=empresa,
            lugar_tipo=lugar_tipo,
            nombre='Test Lugar'
        )
        
        # Test list URL
        response = self.client.get(reverse('lugares:lugar-list'))
        self.assertEqual(response.status_code, 200)
        
        # Test create URL
        response = self.client.get(reverse('lugares:lugar-create'))
        self.assertEqual(response.status_code, 200)
        
        # Test update URL
        response = self.client.get(reverse('lugares:lugar-update', kwargs={'pk': lugar.idLugar}))
        self.assertEqual(response.status_code, 200)
        
        # Test detail URL
        response = self.client.get(reverse('lugares:lugar-detail', kwargs={'pk': lugar.idLugar}))
        self.assertEqual(response.status_code, 200)


class LugaresPaginationTestCase(TestCase):
    """Test cases for pagination in Lugares views"""
    
    def setUp(self):
        self.client = Client()
        
        # Create multiple empresas for pagination testing (15 total)
        for i in range(15):
            Empresa.objects.create(nombre=f'Empresa {i+1}')
        
        # Create empresa and lugar_tipo for lugar testing
        self.empresa = Empresa.objects.create(nombre='Test Empresa')
        self.lugar_tipo = LugarTipo.objects.create(tipo='Laboratorio')
        
        # Create multiple lugares for pagination testing (15 total)
        for i in range(15):
            Lugar.objects.create(
                empresa=self.empresa,
                lugar_tipo=self.lugar_tipo,
                nombre=f'Lugar {i+1}'
            )
    
    def test_empresa_pagination(self):
        """Test Empresa pagination"""
        response = self.client.get(reverse('lugares:empresa-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['empresas']), 10)  # First page
    
    def test_empresa_pagination_second_page(self):
        """Test Empresa pagination second page"""
        response = self.client.get(reverse('lugares:empresa-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['empresas']), 6)  # Second page (16 total - 10 first page)
    
    def test_lugar_pagination(self):
        """Test Lugar pagination"""
        response = self.client.get(reverse('lugares:lugar-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['lugares']), 10)  # First page
    
    def test_lugar_pagination_second_page(self):
        """Test Lugar pagination second page"""
        response = self.client.get(reverse('lugares:lugar-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['lugares']), 5)  # Second page (15 total - 10 first page)