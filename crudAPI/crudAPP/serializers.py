from .models import Category, Product
from rest_framework import serializers



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

        # def to_representation(self,value):
        #     ret = {
        #         "id" : value.id,
        #         "category_name" : value.category_name,
        #     }
        #     return ret

class ProductReadSerializer(serializers.ModelSerializer):
    product_category = CategorySerializer()
    class Meta:
        model = Product
        fields = [ 'id', 'product_name', 'product_category']
       

class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', "product_category"]

        # def create(self,validated_data):
        #     print(validated_data)
        #     prod_name = validated_data.pop("product_name")
        #     cat_id = validated_data.pop("category_id")
        #     cat = Category.objects.filter(id=cat_id)
        #     return Product.objects.create(category=cat,product_name=prod_name, **validated_data)

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=128)

class CatSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    category_name = serializers.CharField(max_length=64)


class CategoryProductSerializer(serializers.Serializer):
    category = CatSerializer()
    product = ProductSerializer(many=True)