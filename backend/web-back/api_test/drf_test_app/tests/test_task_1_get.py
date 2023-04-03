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
        self.GET_URL = "http://localhost:8000/api/v1/task/"
        self.JWT_AUTH_URL = "http://localhost:8000/api/v1/jwt_createtoken/"
        
        # initial_task_data = [{"task":"TEST_TASK_1","smalltask":[{"smalltask":"TEST_SMALLTASK_1"},{"smalltask":"TEST_SMALLTASK_2"}],"motivation":[{"motivation":"TEST_MOTIVATION_1"}]}]
        initial_task_data = [{"task":"task1","smalltask_post":[{"smalltask":"small_0226_1"},{"smalltask":"small_0226_2"}],"motivation_post":[{"motivation":"motivation"}]}]
        initial_user_data = {"email":"admin@admin.com","password":"password"}

        self.saveuser = create_user(**initial_user_data)

        initial_task_data[0]["created_user"] = self.saveuser.id
        
        serializer = TaskSerializer(data=initial_task_data,many=True)
        serializer.is_valid()
        self.savetask = serializer.save()

        # self.savetask = create_task(**initial_create_data)
        # self.GET_URL = "http://localhost:8000/api/v1/task/"
        self.factory = APIRequestFactory()
        self.view = view_task.TaskList.as_view()
        self.token = self.get_token(**initial_user_data)

    def get_token(self,**kwargs):

        view = view_auth.jwt_createtoken.as_view()
        req = self.factory.post(self.JWT_AUTH_URL,json.dumps(kwargs),content_type='application/json')
        res = view(req)

        
        return res.data

    def test_task_1_1_get(self):
        # testdata = {"email":"admin@admin.com","password":"password"}
        # saveuser = create_user(**testdata)

        # url = create_url(self.GET_URL,created_at=self.savetask[0]["created_at"])
        url = create_url(self.GET_URL,created_at=self.savetask[0].created_at)

        request = self.factory.get(url)
        response = self.view(set_token(request, self.token))

        task = Task.objects.filter(task_id=self.savetask[0].task_id)
        # task = Task.objects.filter(task=self.savetask[0]["task"]).prefetch_related().distinct()


        serializer = TaskSerializer(instance=task,many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    # def test_user_1_2_get(self):
    #     request = self.factory.get(create_url(self.GET_URL,userid=uuid.uuid4()))

    #     response = self.view(request)
        
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_user_1_3_get(self):

    #     request = self.factory.get(create_url(self.GET_URL))
        
    #     response = self.view(request)
        
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
       