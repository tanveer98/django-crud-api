import enum
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
 
from ..models import Product
from ..serializers import  (ProductReadSerializer,ProductWriteSerializer)
from .initalize import start
from .GenericRequests import TestSuitMixin

class ProductViewSetTests(TestSuitMixin,TestCase):
    path = "/products/"
    content_type = "application/json"
    serializer = ProductWriteSerializer
    class HTTTPVerb(enum.Enum):
        POST = 1
        PUT = 2

    def setUp(self):
        start()
        return

    def test_get_all(self):
        self.get_all(
            path=self.path,
            model=Product,
            serializer=self.serializer #for get all (.list()), write serializer is being used!
        )
        return
    
    def test_put_post(self):
        # correct post
        verb = self.HTTTPVerb.POST
        self.post_or_put(
            name="P 1",
            field="product_name",
            method=verb,
            http_code=status.HTTP_201_CREATED,
            path=self.path,
            model = Product,
            serializer=self.serializer
        )
        # wrong post
        self.post_or_put(
            name="",
            method=verb,
            field="doge",  # field is wrong
            http_code=status.HTTP_400_BAD_REQUEST,
            path=self.path,
            model = Product,
            serializer=self.serializer
        )
        # correct put
        verb = self.HTTTPVerb.PUT
        pk = 2
        self.post_or_put(
            name="S 3",
            field="product_name",
            method=verb,
            http_code=status.HTTP_200_OK,
            path=f"{self.path}{pk}/",
            model = Product,
            serializer=self.serializer
        )
        # correct put, wrong key
        pk = 10001
        self.post_or_put(
            name="",
            field="product_name",
            method=verb,
            http_code=status.HTTP_404_NOT_FOUND,
            path=f"{self.path}{pk}/",
            model = Product,
            serializer=self.serializer     
        )

    
    def test_delete(self):
        self.del_one(Product,2,self.path)
    
