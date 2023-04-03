from ..models import Task
from ..views import view_task,view_auth
from ..serialyzer import TaskSerializer
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
import uuid
import json
from .test_helper import create_url,create_task,set_token,create_user

class APIViewsTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = view_task.TaskDestroy.as_view()
        self.DELETE_URL = "http://localhost:8000/api/v1/taskdelete/"
        self.JWT_AUTH_URL = "http://localhost:8000/api/v1/jwt_createtoken/"

        initial_user_data = {"email":"admin@admin.com","password":"password"}
        self.saveuser = create_user(**initial_user_data)
        self.token = self.get_token(**initial_user_data)


    def get_token(self,**kwargs):
        view = view_auth.jwt_createtoken.as_view()
        req = self.factory.post(self.JWT_AUTH_URL,json.dumps(kwargs),content_type='application/json')
        res = view(req)        
        return res.data

    def test_task_3_1_delete(self):
        
        initial_task_data = [{"task":"task1","smalltask_post":[{"smalltask":"small_0226_1"},{"smalltask":"small_0226_2"}],"motivation_post":[{"motivation":"motivation"}]}]
        initial_task_data[0]["created_user"] = str(self.saveuser.id)

        serializer = TaskSerializer(data=initial_task_data,many=True)
        serializer.is_valid()
        savetasks = serializer.save()

        self.assertEqual(Task.objects.all().count(), 1)

        request = self.factory.delete(create_url(self.DELETE_URL,created_at=savetasks[0].created_at))
        response = self.view(set_token(request, self.token))


        self.assertEqual(Task.objects.all().count(), 0)
    
        # print(json.dumps(initial_task_data),"initial_task_data#$#[[:[@[@")
        
        # url = create_url(self.CREATE_URL)
        # request = self.factory.post(create_url(self.CREATE_URL),json.dumps(testdata),content_type='application/json') 
        # request = self.factory.post(create_url(self.CREATE_URL),json.dumps(initial_task_data),content_type='application/json')
        # response = self.view(set_token(request, self.token))

        # task = Task.objects.filter(task=initial_task_data[0]["task"])
        # serializer = TaskSerializer(instance=task,many=True)
        # # print(response.data,serializer.data,"¥¥¥¥¥¥¥¥3#$#")
        
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(response.data, serializer.data)
        



        # print(self.savetask,"¥¥¥¥¥¥¥¥3#$#")
        # task = Task.objects.filter(task_id=self.savetask[0]["task_id"])
        # task = Task.objects.filter(task=self.savetask[0]["task"]).prefetch_related().distinct()

        # print("\n\ntask",task)

        # serializer = TaskSerializer(instance=task,many=True)
        # print("\n\nserializer",serializer.data)
        # print("\n\nserializer",response.data)

