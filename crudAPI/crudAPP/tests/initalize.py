from django.test import TestCase
from ..models import (Category, Product)


def start():
    # .create both instantiates and saves object to db.
    Category.objects.create(category_name="Test cat 1")  # pk 1
    Category.objects.create(category_name="Test cat 2")  # pk 2
    Category.objects.create(category_name="Test cat 3")  # pk 3

    cat1 = Category.objects.get(pk=1)
    cat3 = Category.objects.get(pk=3)

    Product.objects.create(product_name="Test prod 1",
                           product_category=cat3)  # pk 1, fk = 3
    Product.objects.create(product_name="Test prod 2",
                           product_category=cat1)  # pk 2, fk = 1
