from Todo_DRF_app.models import Task,CustomUser,TaskList,Project
from Todo_DRF_app.views import authviews
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
from Todo_DRF_app.tests.util.test_helper import create_url,create_task,set_token,create_user,verify_jwt
from rest_framework_simplejwt.tokens import RefreshToken

# アクセストークンを再作成して返すAPIのテスト
class APIViewsTests(TestCase):

    # テスト実行前処理
    def setUp(self):
        self.API_URL = "http://localhost:8000/api/v1/jwt_refresh/"
        self.user = CustomUser.objects.create(email="admin@admin.com",password="password")
        self.token = RefreshToken.for_user(self.user) 
        self.factory = APIRequestFactory()
        self.view = authviews.JWTRefresh.as_view()

    # 正常系
    def test_auth_4_1_refreshtoken(self):
        request = self.factory.get(create_url(self.API_URL))
        response = self.view(set_token(request, self.token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.token.access_token!=response.data['access'], True)
        self.assertEqual(verify_jwt(response.data['access']), True)