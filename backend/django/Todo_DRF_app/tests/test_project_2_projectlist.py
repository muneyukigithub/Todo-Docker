import json

from Todo_DRF_app.models import Task,CustomUser,TaskList,Project
from Todo_DRF_app.views import projectviews
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from rest_framework import status
from Todo_DRF_app.tests.util.test_helper import create_url,create_task,set_token,create_user
from rest_framework_simplejwt.tokens import RefreshToken

# 全てのプロジェクト情報を返すAPIのテスト
class APIViewsTests(TestCase):
    # テスト実行前処理

    def setUp(self):
        self.API_URL = "http://localhost:8000/api/v1/projectlist/"
        self.user = CustomUser.objects.create(email="admin@admin.com",password="password")
        self.token = RefreshToken.for_user(self.user) 
        self.factory = APIRequestFactory()
        self.view = projectviews.ProjectListView.as_view()

    # 正常系
    def test_project_2_1_projectlist(self):

        project1 = Project.objects.create(project="test project1",created_user=self.user)
        tasklist1 = TaskList.objects.create(project=project1,status="waiting",edit=True)
        task1_1 = Task.objects.create(tasklist=tasklist1,tasktype="task",task="test task1")
        task1_2 = Task.objects.create(tasklist=tasklist1,tasktype="subtask",task="test subtask1")

        project2 = Project.objects.create(project="test project2",created_user=self.user)
        tasklist2 = TaskList.objects.create(project=project2,status="waiting",edit=True)
        task2_1 = Task.objects.create(tasklist=tasklist2,tasktype="task",task="test task2")
        task2_2 = Task.objects.create(tasklist=tasklist2,tasktype="subtask",task="test subtask2")

        json_project = json.dumps([{"project":"test project1","projectData":[{"tasklist_id":str(tasklist1.tasklist_id),"edit":True,"status":"waiting","tasklist":[{"task":"test task1","tasktype":"task"},{"task":"test subtask1","tasktype":"subtask"}]}]},{"project":"test project2","projectData":[{"tasklist_id":str(tasklist2.tasklist_id),"edit":True,"status":"waiting","tasklist":[{"task":"test task2","tasktype":"task"},{"task":"test subtask2","tasktype":"subtask"}]}]}])
        
        request = self.factory.get(create_url(self.API_URL,project="test project"))
        response = self.view(set_token(request, self.token))        

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.dumps(response.data), json_project)