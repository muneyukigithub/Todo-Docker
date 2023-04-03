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
        self.CREATETOKEN_URL = "http://localhost:8000/api/v1/jwt_createtoken/"
        self.VERIFY_URL = "http://localhost:8000/api/v1/jwt_verifyrefreshtoken/"
        self.createview = view_auth.jwt_createtoken.as_view()
        self.verifyrefreshtokenview = view_auth.jwt_verifyrefreshtoken.as_view()
        
    # トークンの有効期限を１秒にしてテスト
    def test_auth_3_1_deletetoken(self):
        # DBにユーザー作成
        testuser = {"email":"admin@admin.com","password":"password"}
        testsaveduser = create_user(**testuser)

        # トークン作成
        request = self.factory.post(self.CREATETOKEN_URL,json.dumps(testuser),content_type='application/json')
        response = self.createview(request)
        token = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request = self.factory.get(self.VERIFY_URL)
        response = self.verifyrefreshtokenview(set_token(request, token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_auth_3_2_deletetoken(self):
        # DBにユーザー作成
        testuser = {"email":"admin@admin.com","password":"password"}
        testsaveduser = create_user(**testuser)

        # トークン作成
        request = self.factory.post(self.CREATETOKEN_URL,json.dumps(testuser),content_type='application/json')
        response = self.createview(request)
        token = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        time.sleep(2)

        request = self.factory.get(self.VERIFY_URL)
        response = self.verifyrefreshtokenview(set_token(request, token))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)