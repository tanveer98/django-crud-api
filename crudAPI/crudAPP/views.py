from rest_framework import permissions, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from django.shortcuts import get_object_or_404

from .mixin import ReadWriteSerializerMixin
from .models import Category, Product
from .serializers import (CategorySerializer, ProductReadSerializer,
                          ProductWriteSerializer)


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class ProductViewSet(ReadWriteSerializerMixin,viewsets.ModelViewSet):

    queryset = Product.objects.select_related("category_id").all()
    permission_classes = (AllowAny,)

    #serializer_class = ProductReadSerializer

    ##read serializer
    read_serializer_class = ProductReadSerializer
    ## write serialzier
    write_serializer_class = ProductWriteSerializer
    
    # def list(self, request):
    #     #serializer expects the context so that it can build the url field.
    #     serializer_context = {
    #         'request': request,
    #     }
    #     serialize = ProductReadSerializer(instance=self.queryset, context=serializer_context,many=True)
    #     return Response(data=serialize.data)

    '''
    POST request "controller"
    request.data is a dictionary containing the key and values present in the request
    serialize is a ProdWriteSerializer object, that takes the input dict as a param
    '''
