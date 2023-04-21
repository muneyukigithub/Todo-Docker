from Todo_DRF_app.models import CustomUser
from Todo_DRF_app.views import userviews
from Todo_DRF_app.serialyzer import UserSerializer
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
from Todo_DRF_app.tests.util.test_helper import create_url,create_task,set_token,create_user
from rest_framework_simplejwt.tokens import RefreshToken

# ユーザー情報を削除するAPIのテスト
class APIViewsTests(TestCase):

    # テスト実行前処理
    def setUp(self):
        self.API_URL = "http://localhost:8000/api/v1/userdelete/"
        self.user = CustomUser.objects.create(email="admin@admin.com",password="password")
        self.token = RefreshToken.for_user(self.user) 
        self.factory = APIRequestFactory()
        self.view = userviews.UserDestroy.as_view()

    # 正常系
    def test_user_4_1_userdelete(self):
        request = self.factory.delete(create_url(self.API_URL,userid=self.user.id))
        response = self.view(set_token(request, self.token))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.all().count(), 0)

    # クエリパラメータをつけずにリクエスト
    def test_user_4_2_get(self):

        request = self.factory.delete(create_url(self.API_URL))
        response = self.view(set_token(request, self.token))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.all().count(), 1)