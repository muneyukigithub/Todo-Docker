from ..models import Task
from ..views import view_auth
from ..serialyzer import TaskSerializer
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
import uuid
import json
import time
from .test_helper import create_url,create_task,set_token,create_user

class APIViewsTests(TestCase):

    def setUp(self):
        self.USERINFO_URL = "http://localhost:8000/api/v1/userinfo/"
        self.JWT_AUTH_URL = "http://localhost:8000/api/v1/jwt_createtoken/"

        initial_user_data = {"email":"admin@admin.com","password":"password"}
        self.saveuser = create_user(**initial_user_data)

        self.factory = APIRequestFactory()
        self.view = view_auth.jwt_userinfo.as_view()
        self.token = self.get_token(**initial_user_data)

    def get_token(self,**kwargs):

        view = view_auth.jwt_createtoken.as_view()
        req = self.factory.post(self.JWT_AUTH_URL,json.dumps(kwargs),content_type='application/json')
        res = view(req)
        
        return res.data

    def test_auth_1_1_userinfo(self):
        request = self.factory.get(create_url(self.USERINFO_URL))
        response = self.view(set_token(request, self.token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.saveuser.email)

    def test_auth_1_2_userinfo(self):
        request = self.factory.get(create_url(self.USERINFO_URL))
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        

    # jwtの有効期限の設定を2秒にしてテストする
    def test_auth_1_3_userinfo(self):
        request = self.factory.get(create_url(self.USERINFO_URL))
        time.sleep(2)
        response = self.view(set_token(request, self.token))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
