from rest_framework import serializers
from .models import CustomUser, Task, Project,TaskList
from rest_framework.serializers import SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import APIException
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id','email',"password"]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        unhashed_password = validated_data.pop('password', None)

        new_user = self.Meta.model(**validated_data)

        if unhashed_password is not None:
            new_user.set_password(unhashed_password)
        new_user.save()
        return new_user

    def update(self, pre_update_user, validated_data):

        # 更新されるユーザーのフィールドを入力データの値に書き換えていく
        for field_name, value in validated_data.items():
            if field_name == 'password':
                pre_update_user.set_password(value)
            else:
                setattr(pre_update_user, field_name, value)
        pre_update_user.save()
        return pre_update_user


class TaskDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "task",
            "tasktype"
        ]



class TaskListDeserializer(serializers.ModelSerializer):
    tasklist = SerializerMethodField()
    
    class Meta:
        model = TaskList
        fields = [
            "tasklist_id",
            "edit",
            "status",
            "tasklist",
        ]

    def get_tasklist(self,obj):
        task_obj = Task.objects.filter(tasklist=obj)
        task = TaskDeserializer(instance=task_obj,many=True).data
        return task


class ProjectSerializer(serializers.ModelSerializer):
    projectData = serializers.ListField()

    class Meta:
        model = Project
        fields = [
            "project",
            "projectData",
        ]

    # トランザクション処理 : 複数モデルに書き込むため
    @transaction.atomic
    def create(self,validated_data):

        # エラーハンドリング：保存するプロジェクト名が既にDBにある場合はエラー
        if Project.objects.filter(project=validated_data['project']).exists():
            raise serializers.ValidationError('プロジェクトが既に存在します。')

        
        projectData = validated_data.pop("projectData")

        # プロジェクトモデルの書き込み
        saveproject = Project.objects.create(**validated_data)
        
        # タスクリストモデルの書き込み
        for tasklists in projectData:
            tasklist = tasklists.pop("tasklist")
            tasklists["project"] = saveproject
            savetasklist = TaskList.objects.create(**tasklists)

            # タスクモデルの書き込み
            for task in tasklist:
                task["tasklist"] = savetasklist
                task.pop("checked",None)
                Task.objects.create(**task)
            
        return validated_data





class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "task",
            "tasktype"
        ]

class TodoListSerializer(serializers.ModelSerializer):
    tasklist = TaskSerializer(many=True)

    class Meta:
        model = TaskList
        fields = [
            "tasklist_id",
            "edit",
            "status",
            "tasklist",
        ]

class ProjectDeserializer(serializers.ModelSerializer):
    projectData = TodoListSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            "project",
            "projectData",
        ]






# class ProjectDeserializer(serializers.ModelSerializer):
#     projectData = SerializerMethodField()

#     class Meta:
#         model = Project
#         fields = [
#             "project",
#             "projectData",
#         ]

#     def get_projectData(self,obj):
#         tasklist_obj = TaskList.objects.filter(project=obj)
#         tasklist = TaskListDeserializer(instance=tasklist_obj,many=True).data
#         return tasklist