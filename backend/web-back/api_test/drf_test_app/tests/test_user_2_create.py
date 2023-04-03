from ..models import CustomUser
from ..views import view_user
from ..serialyzer import UserSerializer
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import json
from .test_helper import create_url,create_user

class APIViewsTests(TestCase):

    def setUp(self):
        self.CREATE_URL = "http://localhost:8000/api/v1/create/"
        self.factory = APIRequestFactory()
        self.view = view_user.UserCreate.as_view()
        # self.client = APIClient()

    def test_user_2_1_create(self):
        testdata = {"email":"admin2@admin.com","password":"password"}

        request = self.factory.post(create_url(self.CREATE_URL),json.dumps(testdata),content_type='application/json')
        response = self.view(request)

        user = CustomUser.objects.get(email=testdata["email"])
        serializer = UserSerializer(instance=user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_user_2_2_create(self):
        testdata = {"email":"admin@admin.com"}

        request = self.factory.post(create_url(self.CREATE_URL),json.dumps(testdata),content_type='application/json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_user_2_3_create(self):
        testdata = {"email":"admin@admin.com","password":"password"}
        saveuser = create_user(**testdata)

        request = self.factory.post(create_url(self.CREATE_URL),json.dumps(testdata),content_type='application/json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
        # APIViewsTests.create_user("admin@admin.com", "password")

        # payload = {"email":"admin@admin.com","password":"password"}

        # req = self.factory.post(self.url,json.dumps(payload),content_type='application/json')
        # res = self.view(req)

        # self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        