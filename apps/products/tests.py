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