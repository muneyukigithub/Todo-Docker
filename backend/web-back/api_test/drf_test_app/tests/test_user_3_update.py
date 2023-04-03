from ..models import CustomUser
from ..views import view_user,view_auth
from ..serialyzer import UserSerializer
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
import uuid
import json
from .test_helper import create_url,create_user,set_token


class APIViewsTests(TestCase):
    UPDATE_URL = "http://localhost:8000/api/v1/userupdate/"
    JWT_AUTH_URL = "http://localhost:8000/api/v1/jwt_createtoken/"

    def setUp(self):
        initial_create_data = {"email":"admin@admin.com","password":"password"}
        self.saveuser = create_user(**initial_create_data)
        self.factory = APIRequestFactory()
        self.view = view_user.UserUpdate.as_view()
        self.token = self.get_token(**initial_create_data)

    def get_token(self,**kwargs):

        view = view_auth.jwt_createtoken.as_view()
        req = self.factory.post(self.JWT_AUTH_URL,json.dumps(kwargs),content_type='application/json')
        res = view(req)
        
        return res.data

    def test_user_3_1_update(self):
        update_data = {"email":"update_admin@admin.com","password":"password"}
        request = self.factory.put(create_url(self.UPDATE_URL,userid=self.saveuser.id),json.dumps(update_data),content_type='application/json')
        
        response = self.view(set_token(request, self.token))

        self.saveuser.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.saveuser.email,update_data["email"])

    def test_user_3_2_update(self):
        update_data = {"email":"update_admin@admin.com","password":"update_password"}
        request = self.factory.put(create_url(self.UPDATE_URL,userid=self.saveuser.id),json.dumps(update_data),content_type='application/json')
        
        response = self.view(set_token(request, self.token))

        self.saveuser.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(True,self.saveuser.check_password(update_data["password"]))

    def test_user_3_3_update(self):
        update_data = {"email":"update_admin@admin.com","password":"update_password"}
        request = self.factory.put(create_url(self.UPDATE_URL),json.dumps(update_data),content_type='application/json')
        response = self.view(set_token(request, self.token))

        self.saveuser.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(True,self.saveuser.check_password(self, raw_password),update_data["email"])
    #     payload = {"email":"admin@admin.com","password":"password"}
    #     saveuser = self.create_user(**payload)
    #     token = self.get_token(payload)
    #     view = view_user.UserUpdate.as_view()
        
    #     payload["password"] = "new_password"
    #     req = self.factory.put(self.create_url(self.UPDATE_URL),json.dumps(payload),content_type='application/json')
        
    #     req.COOKIES["access_token"] = token
        
    #     res = view(req)

    #     # updateuser = CustomUser.objects.get(id=saveuser.id)
   
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     # self.assertEqual(True,updateuser.check_password(payload["password"]))

