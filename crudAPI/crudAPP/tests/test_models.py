'''
Module to tests the models of the application
Tests if creating, and retreiving works properly
'''
from django.test import TestCase
from ..models import (Category,Product)
from .initalize import start

#Class to test Category and Product model, a dummy db is created where objects are saved
class ModelTest(TestCase):
    # automatically executed before test starts
    def setUp(self):
        start()
    
    def test_category_model_retireve(self):
        cat = Category.objects.get(pk=2)
        self.assertEqual(str(cat), "Test cat 2")

    def test_product_model_retireve(self):
        prod = Product.objects.get(pk=1)
        self.assertEqual(str(prod),"Test prod 1")

    def test_update(self):
        new_name = "Test cat X"

        #update the name of for foreign key 
        cat = Category.objects.get(pk=1)
        cat.category_name = new_name
        cat.save()

        prod = Product.objects.get(pk=2)
        #retrieved product should now have the updated name of category
        self.assertEqual( str(prod.product_category.category_name) ,new_name)

    def test_delete(self):
        #delete fk of product 1
        cat = Category.objects.get(pk=3)
        cat.delete()
        #product now contains null refernce to category.
        prod = Product.objects.get(pk=1)

        self.assertEqual(prod.product_category, None)

    def test_delete_after_retrieve(self):

        #retriveve product first
        prod = Product.objects.get(pk=1)
        #delete foreign key
        Category.objects.get(pk=3).delete()
        
        #context manager
        with self.assertRaises(Category.DoesNotExist):
            pc = prod.product_category
    