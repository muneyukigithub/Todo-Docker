from Todo_DRF_app.models import Task,CustomUser,TaskList,Project
from Todo_DRF_app.views import authviews
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
from Todo_DRF_app.tests.util.test_helper import create_url,create_task,set_token,create_user,verify_jwt
from rest_framework_simplejwt.tokens import RefreshToken

# JWTトークンを削除するAPIのテスト
class APIViewsTests(TestCase):

    # テスト実行前処理
    def setUp(self):
        self.API_URL = "http://localhost:8000/api/v1/jwt_deletetoken/"
        self.user = CustomUser.objects.create(email="admin@admin.com",password="password")
        self.token = RefreshToken.for_user(self.user) 
        self.factory = APIRequestFactory()
        self.view = authviews.JWTDestroyToken.as_view()
    
    # 正常系
    def test_auth_3_1_deletetoken(self):
        request = self.factory.get(create_url(self.API_URL))
        response = self.view(set_token(request, self.token))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
