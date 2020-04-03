from rest_framework import permissions, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from django.shortcuts import get_object_or_404

from .mixin import ReadWriteSerializerMixin
from .models import Category, Product
from .serializers import (CategorySerializer, ProductReadSerializer,
                          ProductWriteSerializer, CategoryProductSerializer)


'''
"controller classes" aka views(ets), since they inherit from ModelViewSet, they have default implementation
for GET-POST-PUT-DELETE methods.
'''

#Contrller for /category endpoint
class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


#Controller for /products endpoint
class ProductViewSet(ReadWriteSerializerMixin,viewsets.ModelViewSet):

    queryset = Product.objects.select_related("product_category").all()
    permission_classes = (AllowAny,)
    read_serializer_class = ProductReadSerializer
    write_serializer_class = ProductWriteSerializer
    #serializer_class = ProductReadSerializer



class AnotherViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CategoryProductSerializer
    queryset = ''

    def list(self,request):
        # custom = {
        #     "cateogory": <Category Object>,
        #     "product" : [<Product Object>, <Product Object>, ...]
        # }

        list_of_custom = []

        category_qset = Category.objects.all() #get all the categories
        for cat in category_qset:
            custom = {}
            custom["category"] = cat
            custom["product"] = []
            
            prod = cat.product_set.all() #get all the products with this particular category as foreign key

            for p in prod:
                custom["product"].append(p)

            list_of_custom.append(custom)

        serial = CategoryProductSerializer(instance=list_of_custom, many=True)

        return Response(serial.data)

    def retrieve(self, request, pk=None):
        cat = Category.objects.get(pk=pk)

        custom = {}
        custom["category"] = cat
        custom["product"] = []
        
        prod = cat.product_set.all()
        
        for p in prod:
            custom["product"].append(p)
        serial = CategoryProductSerializer(instance=custom)
        
        return Response(serial.data)