import json

from Todo_DRF_app.models import CustomUser,Task,TaskList,Project
from Todo_DRF_app.views import userviews
from Todo_DRF_app.serialyzer import UserSerializer
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from Todo_DRF_app.tests.util.test_helper import create_url,create_user
from django.contrib.auth.hashers import make_password

# ユーザー情報を作成するAPIのテスト
class APIViewsTests(TestCase):

    # テスト実行前処理
    def setUp(self):
        self.API_URL = "http://localhost:8000/api/v1/usercreate/"
        self.factory = APIRequestFactory()
        self.view = userviews.UserCreate.as_view()

    # 正常系
    def test_user_2_1_create(self):
        testdata = {"email":"admin@admin.com","password":"password","password2":"password"}

        request = self.factory.post(create_url(self.API_URL),json.dumps(testdata),content_type='application/json')
        response = self.view(request)

        user = CustomUser.objects.get(email=testdata["email"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, testdata['email'])
        self.assertEqual(user.check_password(testdata['password']),True)