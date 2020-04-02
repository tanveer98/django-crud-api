from .models import Category, Product
from rest_framework import serializers



class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name','url']


class ProductReadSerializer(serializers.HyperlinkedModelSerializer):
    #category_name = serializers.CharField(source='category', read_only=True)
    category_id = CategorySerializer()
    class Meta:
        model = Product
        fields = ['url', 'id', 'product_name', 'category_id']
       

class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['url', 'id', 'product_name', "category_id"]

        def create(self,validated_data):
            print(validated_data)
            prod_name = validated_data.pop("product_name")
            cat_id = validated_data.pop("category_id")
            cat = Category.objects.filter(id=cat_id)

            return Product.objects.create(category=cat,product_name=prod_name, **validated_data)