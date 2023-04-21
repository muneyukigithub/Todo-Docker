from Todo_DRF_app.models import CustomUser,Task,TaskList,Project
from Todo_DRF_app.views import userviews
from Todo_DRF_app.serialyzer import UserSerializer
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
from Todo_DRF_app.tests.util.test_helper import create_url,create_task,set_token,create_user
from rest_framework_simplejwt.tokens import RefreshToken

# ユーザー情報を返すAPIのテスト
class APIViewsTests(TestCase):

    # テスト実行前処理
    def setUp(self):
        self.API_URL = "http://localhost:8000/api/v1/user"
        self.user = CustomUser.objects.create(email="admin@admin.com",password="password")
        self.token = RefreshToken.for_user(self.user) 
        self.factory = APIRequestFactory()
        self.view = userviews.UserRetrieve.as_view()

    # 正常系
    def test_user_1_1_get(self):
        # testdata = {"email":"admin@admin.com","password":"password"}
        # saveuser = create_user(**testdata)

        request = self.factory.get(create_url(self.API_URL,userid=self.user.id))
        response = self.view(set_token(request, self.token))

        user = CustomUser.objects.get(id=self.user.id)
        serializer = UserSerializer(instance=user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    # クエリパラメータをつけずにリクエスト
    def test_user_1_3_get(self):

        request = self.factory.get(create_url(self.API_URL))
        
        response = self.view(set_token(request, self.token))
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
       