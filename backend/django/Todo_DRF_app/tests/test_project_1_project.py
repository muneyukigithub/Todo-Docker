import json

from Todo_DRF_app.models import Task,CustomUser,TaskList,Project
from Todo_DRF_app.views import projectviews
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
from Todo_DRF_app.tests.util.test_helper import create_url,create_task,set_token,create_user
from rest_framework_simplejwt.tokens import RefreshToken

# プロジェクト情報を返すAPIのテスト
class APIViewsTests(TestCase):

    # テスト実行前処理
    def setUp(self):
        self.API_URL = "http://localhost:8000/api/v1/project/"
        self.user = CustomUser.objects.create(email="admin@admin.com",password="password")
        self.token = RefreshToken.for_user(self.user) 
        self.factory = APIRequestFactory()
        self.view = projectviews.ProjectView.as_view()

    # 正常系
    def test_project_1_1_project(self):

        project = Project.objects.create(project="test project",created_user=self.user)
        tasklist = TaskList.objects.create(project=project,status="waiting",edit=True)
        task1 = Task.objects.create(tasklist=tasklist,tasktype="task",task="test task")
        task2 = Task.objects.create(tasklist=tasklist,tasktype="subtask",task="test subtask")

        json_project = json.dumps({"project":"test project","projectData":[{"tasklist_id":str(tasklist.tasklist_id),"edit":True,"status":"waiting","tasklist":[{"task":"test task","tasktype":"task"},{"task":"test subtask","tasktype":"subtask"}]}]})

        request = self.factory.get(create_url(self.API_URL,project="test project"))
        response = self.view(set_token(request, self.token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.dumps(response.data), json_project)