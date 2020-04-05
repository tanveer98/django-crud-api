from rest_framework import permissions, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .mixin import ReadWriteSerializerMixin
from .models import Category, Product
from .serializers import (CategorySerializer, ProductReadSerializer,
                          ProductWriteSerializer, CategoryProductSerializer)
import logging

'''
"controller classes" aka viewsets(or views?), since they inherit from ModelViewSet, they have default implementation
for GET-POST-PUT-DELETE methods, which is mostly sufficent in this context.
'''

# Contrller for /category endpoint


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


# Controller for /products endpoint
class ProductViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):

    queryset = Product.objects.select_related("product_category").all()
    permission_classes = (AllowAny,)
    read_serializer_class = ProductReadSerializer
    write_serializer_class = ProductWriteSerializer

    # reimplemented list method using ProductWriteSerializer
    # so it only displays product_category id value instead of nested category object.
    def list(self, request):
        serializer = ProductWriteSerializer(instance=self.queryset, many=True)
        return Response(serializer.data)


'''
GenericViewSet does not implment the methods required for **ANY** http methods
only methods associated with GET are implemented. So this endpoint only allows get operations.
'''
# Controller for /ProductsByCategory


class CategoryDetailsViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CategoryProductSerializer
    queryset = ''

    # GET all (equivalent to list view?)
    def list(self, request):
        '''
        # custom = {
        #     "cateogory": <Category Object>,
        #     "product" : [<Product Object>, <Product Object>, ...]
        # }
        '''

        try:
            list_of_custom = []
            category_qset = Category.objects.all()  # get all the categories
            for cat in category_qset:
                custom = {}
                custom["category"] = cat
                custom["product"] = []

                # get all the products with this particular category as foreign key
                prod = cat.product_set.all()

                for p in prod:
                    custom["product"].append(p)

                list_of_custom.append(custom)

            serial = CategoryProductSerializer(
                instance=list_of_custom, many=True)
            return Response(serial.data)

        except (Category.DoesNotExist, Product.DoesNotExist) as e:
            logging.warning(e)
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Get one (equivalent to detail view?)
    def retrieve(self, request, pk=None):
        try:
            cat = Category.objects.get(pk=pk)
            custom = {}
            custom["category"] = cat
            custom["product"] = []
            prod = cat.product_set.all()
            for p in prod:
                custom["product"].append(p)
            serial = CategoryProductSerializer(instance=custom)
            return Response(serial.data)

        except (Category.DoesNotExist, Product.DoesNotExist) as e:
            logging.warning(e)
            return Response(status=status.HTTP_404_NOT_FOUND)
