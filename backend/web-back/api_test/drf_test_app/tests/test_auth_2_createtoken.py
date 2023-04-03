from ..views import view_auth
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
import json
from .test_helper import create_url,create_task,set_token,create_user

class APIViewsTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.USERINFO_URL = "http://localhost:8000/api/v1/userinfo/"
        self.CREATETOKEN_URL = "http://localhost:8000/api/v1/jwt_createtoken/"
        self.createview = view_auth.jwt_createtoken.as_view()
        self.userinfoview = view_auth.jwt_userinfo.as_view()

    def test_auth_2_1_createtoken(self):
        # DBにユーザー作成
        testuser = {"email":"admin@admin.com","password":"password"}
        testsaveduser = create_user(**testuser)

        # トークンがない状態でリクエスト
        request = self.factory.get(create_url(self.USERINFO_URL))
        response = self.userinfoview(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # トークン作成
        request = self.factory.post(self.CREATETOKEN_URL,json.dumps(testuser),content_type='application/json')
        response = self.createview(request)
        token = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # トークンがある状態でリクエスト
        request = self.factory.get(create_url(self.USERINFO_URL))
        response = self.userinfoview(set_token(request, token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_2_2_createtoken(self):
        # DBにユーザー作成
        testuser = {"email":"admin@admin.com","password":"password"}
        testsaveduser = create_user(**testuser)

        # 存在しないユーザーを定義
        testuser = {"email":"test@test.com","password":"password"}

        # 存在しないユーザーでトークン作成リクエスト
        request = self.factory.post(self.CREATETOKEN_URL,json.dumps(testuser),content_type='application/json')
        response = self.createview(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)