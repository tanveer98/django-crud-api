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


class CategoryViewSetTest(TestCase):
    path = "/category/"
    content_type = "application/json"

    class HTTTPVerb(enum.Enum):
        POST = 1
        PUT = 2

    def setUp(self):
        start()

    def test_get_all(self):
        resp = APIClient().get(path=self.path).data
        categories = Category.objects.all()
        db_data = CategorySerializer(instance=categories, many=True).data
        self.assertEqual(resp, db_data)  # data from db matches api response!
        return

    def post_or_put(self, name, method, http_code, field="category_name", path="/category/"):
        mime = "application/json"
        payload = json.dumps({
            field: name
        })

        resp = None
        cat_name = ""
        if method is self.HTTTPVerb.POST:
            resp = APIClient().post(path=path, data=payload, content_type=mime)

        elif method is self.HTTTPVerb.PUT:
            resp = APIClient().put(path=path, data=payload, content_type=mime)

        try:
            cat = Category.objects.get(category_name=name)
            cat_name = cat.category_name
        except BaseException as e:
            print(e)

        self.assertEqual(resp.status_code, http_code, "wrong code")
        self.assertEqual(name, cat_name, "wrong name")

    def test_put_post(self):
        # correct post
        verb = self.HTTTPVerb.POST
        self.post_or_put(
            name="S 1",
            method=verb,
            http_code=status.HTTP_201_CREATED
        )
        # wrong post
        self.post_or_put(
            name="",
            method=verb,
            field="doge",  # field is wrong
            http_code=status.HTTP_400_BAD_REQUEST
        )
        # correct put
        verb = self.HTTTPVerb.PUT
        pk = 2
        self.post_or_put(
            name="S 3",
            method=verb,
            path=f"{self.path}{pk}/",
            http_code=status.HTTP_200_OK
        )
        # correct put, wrong key
        pk = 10001
        self.post_or_put(
            name="",
            method=verb,
            path=f"{self.path}{pk}/",
            http_code=status.HTTP_404_NOT_FOUND
        )

    def test_delete(self):
        pk = 2
        del_path = f"{self.path}{pk}/"
        resp = APIClient().delete(del_path)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        cat = None
        #test if trying to retrieve deleted item throws exception or not
        with self.assertRaises(Category.DoesNotExist):
            cat = Category.objects.get(pk=2) 
