from ..models import CustomUser
from ..views import view_user,view_auth
from ..serialyzer import UserSerializer
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
import uuid
import json
from .test_helper import create_url,create_user,set_token


class APIViewsTests(TestCase):
    DELETE_URL = "http://localhost:8000/api/v1/userdelete/"
    JWT_AUTH_URL = "http://localhost:8000/api/v1/jwt_createtoken/"

    def setUp(self):
        initial_create_data = {"email":"admin@admin.com","password":"password"}
        self.saveuser = create_user(**initial_create_data)
        self.factory = APIRequestFactory()
        self.view = view_user.UserDestroy.as_view()
        self.token = self.get_token(**initial_create_data)

    def get_token(self,**kwargs):

        view = view_auth.jwt_createtoken.as_view()
        req = self.factory.post(self.JWT_AUTH_URL,json.dumps(kwargs),content_type='application/json')
        res = view(req)
        
        return res.data

    def test_user_4_1_update(self):        
        self.assertEqual(CustomUser.objects.all().count(),1)
        
        request = self.factory.delete(create_url(self.DELETE_URL,userid=self.saveuser.id))
        response = self.view(set_token(request, self.token))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.all().count(),0)

    def test_user_4_2_update(self):
        request = self.factory.delete(create_url(self.DELETE_URL))
        response = self.view(set_token(request, self.token))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(CustomUser.objects.all().count(),0)

    def test_user_4_3_update(self):
        request = self.factory.delete(create_url(self.DELETE_URL,userid=uuid.uuid4()))
        response = self.view(set_token(request, self.token))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # payload = {"email":"admin@admin.com","password":"password"}
        # saveuser = self.create_user(**payload)

        # request = self.factory.delete(self.create_url(self.DELETE_URL,userid=uuid.uuid4()))
        # response = self.send_request(self.view, request, self.get_token(payload))

        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # def _test_user_4_1_update(self):
    #     payload = {"email":"admin@admin.com","password":"password"}
    #     saveuser = self.create_user(**payload)
        
    #     self.assertEqual(CustomUser.objects.all().count(),1)
        
    #     request = self.factory.delete(self.create_url(self.DELETE_URL,userid=saveuser.id))
    #     response = self.send_request(self.view, request, self.get_token(payload))

    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(CustomUser.objects.all().count(),0)


    # def test_user_4_2_update(self):
    #     payload = {"email":"admin@admin.com","password":"password"}
    #     saveuser = self.create_user(**payload)

    #     request = self.factory.delete(self.create_url(self.DELETE_URL))
    #     response = self.send_request(self.view, request, self.get_token(payload))

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     # self.assertEqual(CustomUser.objects.all().count(),0)

    # def test_user_4_3_update(self):
    #     payload = {"email":"admin@admin.com","password":"password"}
    #     saveuser = self.create_user(**payload)

    #     request = self.factory.delete(self.create_url(self.DELETE_URL,userid=uuid.uuid4()))
    #     response = self.send_request(self.view, request, self.get_token(payload))

    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)