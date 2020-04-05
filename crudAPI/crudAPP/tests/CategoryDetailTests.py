from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
 
from ..models import (Category,Product)
from ..serializers import (CategoryProductSerializer,ProductSerializer)
from .initalize import start

class CategoryDetailViewSetTest(TestCase):
    path = "/category-details/"
    def setUp(self):
        start()
        pass
    
    def test_get_all(self):
        resp = APIClient().get(path=self.path)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    def test_get_one(self):
        pk = 1
        resp = APIClient().get(path=f"{self.path}{pk}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        prod_id = resp.data['product'][0]['id']
        self.assertEqual(prod_id, 2) #becasue prod pk = 2 has category pk = 1 as foreign key field!