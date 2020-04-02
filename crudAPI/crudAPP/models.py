from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=64)
    
    def __str__(self):
        str_ = self.category_name
        return str_
class Product(models.Model):
    category_id = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, db_column='category_id')
    product_name = models.CharField(max_length=128)

    def __str__(self):
        str_ = self.product_name
        return str_
