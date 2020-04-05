from .models import Category, Product
from rest_framework import serializers

'''
To serialize Category models 9for both read/write ops
'''
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

'''
ReadSerializer for GET (read) methods
'''
class ProductReadSerializer(serializers.ModelSerializer):
    product_category = CategorySerializer()
    class Meta:
        model = Product
        fields = [ 'id', 'product_name', 'product_category']
       
'''
WriteSerializer for POST/PUT methods
'''
class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', "product_category"]


'''
Normal (non model) serializer, for product field ProductRead/Write Serializer could also be used
Non model is implemented to not display redundant product_category field 
(which would be displayed if ProductRead or ProductWrite serialzier was used.)
'''
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=128)


class CategoryProductSerializer(serializers.Serializer):
    category = CategorySerializer()
    product = ProductSerializer(many=True)