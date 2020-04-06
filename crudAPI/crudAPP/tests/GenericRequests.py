import enum
import json
from rest_framework import status
from rest_framework.test import APIClient


from ..models import (Category,Product)
'''
All hail python generics!
'''
class TestSuitMixin(object):

    def get_all(self, path, model, serializer):
        resp = APIClient().get(path=path).data
        queryset = model.objects.all()
        model_list = serializer(instance=queryset, many=True).data
        self.assertEqual(resp, model_list)
        return

    def post_or_put(self, name, field, method, http_code, path, model, serializer):
        mime = "application/json"
        payload = json.dumps({
            field: name
        })


        resp = None
        model_name = ""
        if method is self.HTTTPVerb.POST:
            resp = APIClient().post(path=path, data=payload, content_type=mime)

        elif method is self.HTTTPVerb.PUT:
            resp = APIClient().put(path=path, data=payload, content_type=mime)

        try:
            mod = None
            if isinstance(model(),Category):
                mod = model.objects.get(category_name=name)
            elif isinstance(model(),Product):
                mod = model.objects.get(product_name=name)
            else:
                print("wrong model")

            model_name = getattr(mod, field) # get model.poduct_name or model.category_name
        
        except BaseException as e:
            print(e)

        self.assertEqual(resp.status_code, http_code, "wrong code")
        self.assertEqual(name, model_name, "wrong name")

    def del_one(self, model,pk,base_path):
        path = f"{self.path}{pk}/"
        resp = APIClient().delete(path)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        #test if trying to retrieve deleted item throws exception or not
        with self.assertRaises(model.DoesNotExist):
            model.objects.get(pk=2)

