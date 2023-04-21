import json

from Todo_DRF_app.models import Task,CustomUser,TaskList,Project
from Todo_DRF_app.views import projectviews
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
from Todo_DRF_app.tests.util.test_helper import create_url,create_task,set_token,create_user
from rest_framework_simplejwt.tokens import RefreshToken

# プロジェクト情報を作成するAPIのテスト
class APIViewsTests(TestCase):

    # テスト実行前処理
    def setUp(self):
        self.API_URL = "http://localhost:8000/api/v1/userupdate/"
        self.user = CustomUser.objects.create(email="admin@admin.com",password="password")
        self.token = RefreshToken.for_user(self.user) 
        self.factory = APIRequestFactory()
        self.view = projectviews.ProjectCreateView.as_view()

    # 正常系
    def test_project_3_1_projectcreate(self):
        # 保存用のプロジェクト情報
        test_project = {"project": "test project", "projectData": [{"edit": True, "status": "waiting", "tasklist": [{"task": "test task", "tasktype": "task"}, {"task": "test subtask", "tasktype": "subtask"}]}]}

        request = self.factory.post(create_url(self.API_URL),json.dumps(test_project),content_type='application/json') 
        response = self.view(set_token(request, self.token))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.all().count(),1)
        self.assertEqual(Project.objects.first().project,test_project['project'])
        self.assertEqual(TaskList.objects.all().count(),1)
        self.assertEqual(TaskList.objects.first().edit,True)
        self.assertEqual(TaskList.objects.first().status,"waiting")
        self.assertEqual(Task.objects.all().count(),2)
        self.assertEqual(Task.objects.get(task="test task").task,"test task")
        self.assertEqual(Task.objects.get(task="test task").tasktype,"task")
        self.assertEqual(Task.objects.get(task="test subtask").task,"test subtask")
        self.assertEqual(Task.objects.get(task="test subtask").tasktype,"subtask")