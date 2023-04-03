from ..models import CustomUser
from ..views import view_user
from ..serialyzer import UserSerializer
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
import uuid
from .test_helper import create_url,create_user

class APIViewsTests(TestCase):

    def setUp(self):
        self.GET_URL = "http://localhost:8000/api/v1/user"
        self.factory = APIRequestFactory()
        self.view = view_user.UserRetrieve.as_view()

    def test_user_1_1_get(self):
        testdata = {"email":"admin@admin.com","password":"password"}
        saveuser = create_user(**testdata)

        request = self.factory.get(create_url(self.GET_URL,userid=saveuser.id))
        response = self.view(request)

        user = CustomUser.objects.get(id=saveuser.id)
        serializer = UserSerializer(instance=user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_user_1_2_get(self):
        request = self.factory.get(create_url(self.GET_URL,userid=uuid.uuid4()))

        response = self.view(request)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_1_3_get(self):

        request = self.factory.get(create_url(self.GET_URL))
        
        response = self.view(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
       