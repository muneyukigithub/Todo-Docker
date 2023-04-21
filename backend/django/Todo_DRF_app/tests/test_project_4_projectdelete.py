import json

from Todo_DRF_app.models import Task,CustomUser,TaskList,Project
from Todo_DRF_app.views import projectviews
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
from Todo_DRF_app.tests.util.test_helper import create_url,create_task,set_token,create_user
from rest_framework_simplejwt.tokens import RefreshToken

# プロジェクト情報を削除するAPIのテスト
class APIViewsTests(TestCase):

    # テスト実行前処理
    def setUp(self):
        self.API_URL = "http://localhost:8000/api/v1/projectdelete/"
        self.user = CustomUser.objects.create(email="admin@admin.com",password="password")
        self.token = RefreshToken.for_user(self.user) 
        self.factory = APIRequestFactory()
        self.view = projectviews.ProjectDeleteView.as_view()

    # 正常系
    def test_project_4_1_projectdelete(self):

        project = Project.objects.create(project="test project",created_user=self.user)
        tasklist = TaskList.objects.create(project=project,status="waiting",edit=True)
        task1 = Task.objects.create(tasklist=tasklist,tasktype="task",task="test task")
        task2 = Task.objects.create(tasklist=tasklist,tasktype="subtask",task="test subtask")

        request = self.factory.delete(create_url(self.API_URL,project="test project"))
        response = self.view(set_token(request, self.token))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.filter(id=project.pk).exists(), False)
        self.assertEqual(TaskList.objects.filter(tasklist_id=tasklist.tasklist_id).exists(), False)
        self.assertEqual(Task.objects.filter(id=task1.pk).exists(), False)
        self.assertEqual(Task.objects.filter(id=task2.pk).exists(), False)

