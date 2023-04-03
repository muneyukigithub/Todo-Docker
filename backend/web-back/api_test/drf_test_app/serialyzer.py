from rest_framework import serializers
from .models import CustomUser, Task, Project,TaskList
from rest_framework.serializers import SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password


# class myTokenObtainPairSerializer:
#     TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id','email']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # print("create!!!")
        # print(validated_data)

        unhashed_password = validated_data.pop('password', None)

        new_user = self.Meta.model(**validated_data)

        if unhashed_password is not None:
            new_user.set_password(unhashed_password)
        new_user.save()
        return new_user

    def update(self, pre_update_user, validated_data):
        # print("update!!!")
        # 更新されるユーザーのフィールドを入力データの値に書き換えていく
        for field_name, value in validated_data.items():
            # passwordを更新する際は入力データの値をset_password()の引数に渡してハッシュ化
            if field_name == 'password':
                pre_update_user.set_password(value)
            # password以外のフィールドを更新する際は入力データでそのまま上書きでOK
            else:
                setattr(pre_update_user, field_name, value)
        pre_update_user.save()
        return pre_update_user


# projectのjson情報をシリアライズする。
# project情報をmodel化して保存する。保存したモデルを取得
# 


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "task",
            "tasktype"
        ]



class TaskListSerializer(serializers.ModelSerializer):
    # tasklist = serializers.ListField(child=TaskSerializer)
    
    class Meta:
        model = TaskList
        fields = [
            # "tasklist",
            "tasklist_id",
            "edit",
            "status",
        ]

class ProjectDeserializer(serializers.ModelSerializer):
    # projectData = SerializerMethodField()
    # projectData = serializers.ListField()

    class Meta:
        model = Project
        fields = [
            "project",
            # "created_at"
            # "projectData",
        ]

class ProjectSerializer(serializers.ModelSerializer):
    # projectData = SerializerMethodField()
    projectData = serializers.ListField()

    class Meta:
        model = Project
        fields = [
            "project",
            "projectData",
        ]
    


    def create(self,validated_data):
        print(validated_data)
        try:
            model_confirm = Project.objects.get(project=validated_data["project"])
            print("1")

            raise Exception("このプロジェクトは既に存在する")
        except Project.DoesNotExist:
            print("2")

            pass
        except:
            print("3")

            raise Exception("このプロジェクトは既に存在する")


        projectData = validated_data.pop("projectData")
        
        saveproject = Project.objects.create(**validated_data)
        
        for tasklists in projectData:

            tasklist = tasklists.pop("tasklist")

            tasklists["project"] = saveproject
            savetasklist = TaskList.objects.create(**tasklists)

            for task in tasklist:
                task["tasklist"] = savetasklist
                Task.objects.create(**task)
            
        return validated_data






    # def create(self, validated_data):
    #     print("create call is SmallTask(**validate")
    #     return SmallTask(**validated_data)
# class SmallTaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SmallTask
#         # fields = "__all__"
#         fields = ["smalltask",]
#         extra_kwargs = {
#             'task_id': {'write_only': True},
#         }
#         # fields = ("smalltask_id", "smalltask", "task_id")

    
# class MotivationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Motivation
#         # fields = "__all__"
#         fields = ["motivation",]
#         extra_kwargs = {
#             'task_id': {'write_only': True},
#         }
        # read_only_fields = ('created_at', 'updated_at')
# class __TaskSerializer(serializers.ModelSerializer):
#     # SerializerMethodField は get_xxxx ってなっているメソッドをコールする
#     # smalltask = SerializerMethodField()
#     smalltask = SmallTaskSerializer(many=True)
#     # motivation = SerializerMethodField()
#     motivation = MotivationSerializer()


#     # smalltask = SmallTaskSerializer(many=True,read_only=False)
#     # motivation = MotivationSerializer(many=True,read_only=False)

#     class Meta:
#         model = Task
#         fields = [
#             "task",
#             "task_id",
#             "smalltask",
#             "motivation",
#             "created_user",
#             "created_at",
#         ]
#         # extra_kwargs = {
#         #     'created_user': {'write_only': True},
#         # }

#     def get_smalltask(self, obj):
#         # print(obj)
#         # print("70",type(obj))
#         # print(obj)
#         # print("--------",type(obj))
#         # tmp_model = SmallTask.objects.all().filter(task_id=obj["task_id"])
#         tmp_model = SmallTask.objects.all().filter(task_id=obj.task_id)

#         return SmallTaskSerializer(instance=tmp_model,many=True).data
    
#     def get_motivation(self,obj):
#         # tmp_model = Motivation.objects.all().filter(task_id=obj["task_id"])
#         tmp_model = Motivation.objects.all().filter(task_id=obj.task_id)
#         # print("tmp_model:",obj.task_id)

#         return MotivationSerializer(instance=tmp_model,many=True).data

#     def create(self, validated_data):
#         return_data = {}

#         ModelClass = self.Meta.model
#         task = ModelClass._default_manager.create(task=validated_data["task"],created_user=validated_data["created_user"])

#         smalltask_datalist = []
#         for smalltask in validated_data["smalltask"]:
#             smalltask = SmallTask.objects.create(task_id=task,smalltask=smalltask["smalltask"])
#             smalltask_datalist.append({"smalltask":smalltask.smalltask})
            
#         motivation = Motivation.objects.create(task_id=task,motivation=validated_data["motivation"]["motivation"])

#         return_data["task"] = task.task
#         return_data["task_id"] = task.task_id
#         return_data["smalltask"] = smalltask_datalist
#         # return_data["motivation"] = {"motivation":motivation.motivation}
#         return_data["motivation"] = {"motivation":motivation.motivation}
#         return_data["created_user"] = task.created_user

#         return return_data


# class _TaskSerializer(serializers.ModelSerializer):
#     smalltask = SerializerMethodField()
#     motivation = SerializerMethodField()
#     smalltask_post = SmallTaskSerializer(many=True,write_only=True)
#     motivation_post = MotivationSerializer(many=True,write_only=True)

#     class Meta:
#         model = Task
#         fields = [
#             "task",
#             "task_id",
#             "smalltask",
#             "smalltask_post",
#             "motivation",
#             "motivation_post",
#             "created_user",
#             "created_at",
#         ]
#         read_only_fields = ('task_id',)

#     def get_smalltask(self, obj):
#         # tmp_model = SmallTask.objects.all().filter(task_id=obj["task_id"])

#         try:
#             tmp_model = SmallTask.objects.all().filter(task_id=obj)
#         except Exception as e:
#             raise e

#         return SmallTaskSerializer(instance=tmp_model,many=True).data
    
#     def get_motivation(self,obj):
#         # tmp_model = Motivation.objects.all().filter(task_id=obj["task_id"])
#         tmp_model = Motivation.objects.all().filter(task_id=obj)

#         return MotivationSerializer(instance=tmp_model,many=True).data

#     def create(self, validated_data):

#         def create_dict(**kwargs):
#             tmp_dict = {}
#             for key,value in kwargs.items():
#                 tmp_dict[key] = value
#             return tmp_dict


#         # for data in validated_data:
#         #     print(data ,"@@@@@@@@@validated_data")

#         task,smalltask_post,motivation_post,created_user = validated_data.values()

#         saved_task = Task.objects.create(**create_dict(task=task,created_user=created_user))

#         smalltask_list = []
#         for smalltask in smalltask_post:
#             saved_smalltask = SmallTask.objects.create(**create_dict(**smalltask,task_id=saved_task))
#             smalltask_list.append(create_dict(smalltask=saved_smalltask.smalltask))

#         motivation_list = []
#         for motivation in motivation_post:
#             saved_motivation = Motivation.objects.create(**create_dict(**motivation,task_id=saved_task))
#             # print(saved_motivation,"@@@@@@@@@saved_motivation")
            
#             motivation_list.append(create_dict(motivation=saved_motivation.motivation))

#         # s = TaskSerializer(instance=saved_task)
#         return saved_task

    
# class RegisterUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         # fields = ["email"]
#         fields = "__all__"

#         # extra_kwargsは読み込みはせず、書き込みだけしたいフィールドを記載
#         extra_kwargs = {
#             "password": {"write_only": True},
#         }

#         # 追加

#     def validate_password(self, value: str) -> str:
#         """
#         ハッシュ値に変換する
#         """
#         return make_password(value)
