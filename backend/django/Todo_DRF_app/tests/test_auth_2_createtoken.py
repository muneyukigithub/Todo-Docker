import json

from Todo_DRF_app.models import Task,CustomUser,TaskList,Project
from Todo_DRF_app.views import authviews
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
from Todo_DRF_app.tests.util.test_helper import create_url,create_task,set_token,create_user,verify_jwt
from rest_framework_simplejwt.tokens import RefreshToken

# JWTトークンを作成して返すAPIのテスト
class APIViewsTests(TestCase):

    # テスト実行前処理
    def setUp(self):
        self.API_URL = "http://localhost:8000/api/v1/jwt_createtoken/"
        self.user = CustomUser.objects.create(email="admin@admin.com",password="password")
        self.factory = APIRequestFactory()
        self.view = authviews.JWTCreateToken.as_view()


    # 正常系
    def test_auth_2_1_createtoken(self):
        user = {"email":"admin@admin.com","password":"password"}
        request = self.factory.post(self.API_URL,json.dumps(user),content_type='application/json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(verify_jwt(response.data['access']), True)
        self.assertEqual(verify_jwt(response.data['refresh']), True)

    # トークンを作成するための認証情報に不備があるパターン
    def test_auth_2_2_createtoken(self):
        user = {"email":"admin_dummy@admin.com","password_dummy":"password"}
        request = self.factory.post(self.API_URL,json.dumps(user),content_type='application/json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(verify_jwt(response.data.get('access')), False)
        self.assertEqual(verify_jwt(response.data.get('refresh')), False)
        