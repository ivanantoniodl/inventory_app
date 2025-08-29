from django.test import TestCase

# Create your tests here.
from .models import Categoria, Medida
from django.urls import reverse

class CategoriaListViewTestCase(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(categoria='Categoria Teste', habilitado=True, es_producto=True)
        self.categoria = Categoria.objects.create(categoria='Reactivos', habilitado=True, es_producto=True)

    def test_categoria_count(self):
        self.assertEqual(Categoria.objects.count(), 2)

class CategoriaCreateViewTestCase(TestCase):
    def test_categoria_create_view(self):
        response = self.client.post(reverse('productos:categoria-create'), {
            'categoria': 'Insumos',
        })
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertEqual(Categoria.objects.count(), 1)
        self.assertEqual(Categoria.objects.first().categoria, 'Insumos')
        self.assertTrue(Categoria.objects.first().habilitado)
        self.assertTrue(Categoria.objects.first().es_producto)

class MedidaCreateViewTestCase(TestCase):
    def test_medida_create_view(self):
        response = self.client.post(reverse('productos:medida-create'), {
            'medida': 'Litros',
        })
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertEqual(Medida.objects.count(), 1)
        self.assertEqual(Medida.objects.first().medida, 'Litros')
        self.assertTrue(Medida.objects.first().es_producto)