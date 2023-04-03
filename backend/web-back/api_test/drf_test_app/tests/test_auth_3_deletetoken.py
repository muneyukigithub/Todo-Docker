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
        self.factory = APIRequestFactory()
        self.USERINFO_URL = "http://localhost:8000/api/v1/userinfo/"
        self.CREATETOKEN_URL = "http://localhost:8000/api/v1/jwt_createtoken/"
        self.DELETETOKEN_URL = "http://localhost:8000/api/v1/jwt_deletetoken/"
        self.createview = view_auth.jwt_createtoken.as_view()
        self.deleteview = view_auth.jwt_destroytoken.as_view()
        

    def test_auth_3_1_deletetoken(self):
        # DBにユーザー作成
        testuser = {"email":"admin@admin.com","password":"password"}
        testsaveduser = create_user(**testuser)

        # トークン作成
        request = self.factory.post(self.CREATETOKEN_URL,json.dumps(testuser),content_type='application/json')
        response = self.createview(request)
        token = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # トークン削除
        request = self.factory.get(create_url(self.DELETETOKEN_URL))
        response = self.deleteview(set_token(request, token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.cookies["access_token"]["max-age"], 0)
        self.assertEqual(response.cookies["refresh_token"]["max-age"], 0)