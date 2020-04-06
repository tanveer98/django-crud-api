'''
Test class to test views
'''

import json
import enum
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase

from ..models import Category
from ..serializers import CategorySerializer
from .initalize import start
from .GenericRequests import  TestSuitMixin


class CategoryViewSetTest(TestSuitMixin,TestCase):
    path = "/category/"
    content_type = "application/json"

    class HTTTPVerb(enum.Enum):
        POST = 1
        PUT = 2

    def setUp(self):
        start()

    def test_get_all(self):
        self.get_all(
            path=self.path,
            model=Category,
            serializer=CategorySerializer
        )
        return

    def test_put_post(self):
        # correct post
        verb = self.HTTTPVerb.POST
        self.post_or_put(
            name="S 1",
            field="category_name",
            method=verb,
            http_code=status.HTTP_201_CREATED,
            path=self.path,
            model = Category,
            serializer=CategorySerializer
        )

        # wrong post
        self.post_or_put(
            name="",
            method=verb,
            field="doge",  # field is wrong
            http_code=status.HTTP_400_BAD_REQUEST,
            path=self.path,
            model = Category,
            serializer=CategorySerializer
        )
        # correct put
        verb = self.HTTTPVerb.PUT
        pk = 2
        self.post_or_put(
            name="S 3",
            field="category_name",
            method=verb,
            http_code=status.HTTP_200_OK,
            path=f"{self.path}{pk}/",
            model = Category,
            serializer=CategorySerializer
        )
        # correct put, wrong key
        pk = 10001
        self.post_or_put(
            name="",
            field="category_name",
            method=verb,
            http_code=status.HTTP_404_NOT_FOUND,
            path=f"{self.path}{pk}/",
            model = Category,
            serializer=CategorySerializer     
        )

    
    def test_delete(self):
        self.del_one(Category,2,self.path)