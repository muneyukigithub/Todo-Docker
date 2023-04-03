from django.shortcuts import render
from rest_framework import viewsets
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt import exceptions as jwt_exp
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
import jwt
from django.conf import settings
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from ..authentication import CookieHandlerJWTAuthentication
# from .authentication import CookieHandlerJWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime,timezone
import time

from rest_framework.generics import DestroyAPIView,UpdateAPIView,ListAPIView,RetrieveAPIView,CreateAPIView
from rest_framework.response import Response
from rest_framework import exceptions as drf_exp
from rest_framework import status
from ..serialyzer import TaskSerializer,ProjectSerializer,TaskListSerializer,ProjectDeserializer
from django.conf import settings
from ..models import CustomUser,Project,TaskList,Task


# def base64decode(encodetext):
#     textBytes = base64.b64decode(encodetext.encode())
#     return textBytes.decode()

# class TaskList(ListAPIView):
#     authentication_classes = (CookieHandlerJWTAuthentication,)
#     permission_classes = [IsAuthenticated,]
#     queryset = TaskModel.objects.all()
#     serializer_class = TaskSerializer

#     def get(self, request, *args, **kwargs):

#         created_at = request.GET.get("created_at",None)
#         if created_at:
#             self.kwargs["created_at"] = created_at

#         self.kwargs['created_user'] = self.request.user.id

#         return self.list(request, *args, **kwargs)

#     def get_queryset(self,**kwargs):
#         queryset = self.queryset.filter(**self.kwargs)

        # print("queryset1        ",queryset,self.kwargs)

        # new_query = []
        # for task_q in queryset:
        #     print("::::::task_q::::::",task_q)

        #     tmp_dict = {}
        #     s = SmallTask.objects.filter(task_id=task_q)

        #     smalltask = SmallTaskSerializer(instance=s,many=True)
        #     m = Motivation.objects.get(task_id=task_q)
        #     motivation = MotivationSerializer(instance=m)

        #     tmp_dict["task"] = task_q.task
        #     tmp_dict["task_id"] = task_q.task_id

        #     tmp_dict["smalltask"] = smalltask.data
        #     # tmp_dict["motivation"] = {"motivation":motivation.motivation}
        #     tmp_dict["motivation"] = motivation.data
        #     tmp_dict["created_user"] = task_q.created_user
        #     tmp_dict["created_at"] = task_q.created_at


        #     new_query.append(tmp_dict)

        # print("::::::new_::::::",new_query)

        # queryset = queryset.filter(**self.kwargs)
        # print("queryset2        ",queryset,self.kwargs)

    #     return queryset

    # def list(self, request, *args, **kwargs):
    #     # queryset = self.filter_queryset(self.get_queryset())
    #     queryset = self.get_queryset()



    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)


    #     serializer = self.get_serializer(queryset, many=True)
    #     # print("self.instance:        ",serializer.instance)
    #     return Response(serializer.data)
    
        # if not created_at:
        #     # raise ValueError("error!")
        #     return Response({"error": "パラメータが指定されていません"}, status=400)

        # userid = request.GET.get("taskid")
        # if not userid:
        #     return Response({"error": "ユーザIDが指定されていません"}, status=400)

        # self.kwargs["task_id"] = userid
     

        # print(self.kwargs['created_user'])
        # if self.kwargs['created_user']:
        #     return Response({"error": "パラメータが指定されていません"}, status=400)




        # url_params = self.request.GET.get("created_at")
        # print(self.request.user)
        # print(self.request.auth)

        # if not url_params:
            # raise ValueError("error!")

            # return Response({"error": "パラメータが指定されていません"}, status=400)

        # self.kwargs['created_at']=url_params
        # self.kwargs['created_user']=self.request.user

        # return self.list(request, *args, **kwargs)

# class no__TaskRetrieve(ListAPIView):
#     authentication_classes = (CookieHandlerJWTAuthentication,)
#     permission_classes = [IsAuthenticated,]
#     queryset = TaskModel.objects.all()
#     serializer_class = TaskSerializer
#     # lookup_field = ""

#     def get(self, request, *args, **kwargs):
#         created_at = request.GET.get("created_at")
#         # print(self.request.user)
#         # print(self.request.auth)

#         if not created_at:
#             # raise ValueError("error!")
#             return Response({"error": "パラメータが指定されていません"}, status=400)

#         self.kwargs['created_at']=created_at
#         self.kwargs['created_user']=self.request.user

#         return self.list(request, *args, **kwargs)

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)


#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

#     def get_queryset(self,**kwargs):
#         queryset = self.queryset

#         queryset = queryset.filter(**self.kwargs)

#         assert self.queryset is not None, (
#             "'%s' should either include a `queryset` attribute, "
#             "or override the `get_queryset()` method."
#             % self.__class__.__name__
#         )

#         return queryset


        # if isinstance(queryset, QuerySet):
        #     # Ensure queryset is re-evaluated on each request.

        # queryset = queryset.all()

from ..serialyzer import ProjectSerializer
from django.conf import settings
from logging import getLogger,config
config.dictConfig(settings.LOGGING)
logger = getLogger(__name__)
import time

# from logging import getLogger,config
# config.dictConfig(settings.LOGGING)
# logger = getLogger(__name__)
class ProjectListView(generics.ListAPIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = [IsAuthenticated,]

    serializer_class = ProjectDeserializer
    queryset = Project.objects.all()

    def get_queryset(self):
        # print(self.request.user)
        queryset = self.queryset.all().filter(created_user=self.request.user)
        return queryset

    


class ProjectView(generics.GenericAPIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = [IsAuthenticated,]
    # permission_classes=(IsAuthenticated)
    # queryset = Project.objects
    serializer_class = ProjectSerializer

    def get(self,request):
        project = request.GET.get("project",None)

        # logger.debug(project,request.user)

        if(project==None):
            return Response({"error":"プロジェクト名が指定されていません。"},status.HTTP_400_BAD_REQUEST)

        try:
            # project_queryset = Project.objects.get(project=project,created_user=request.user)
            project_queryset = Project.objects.get(project=project)
        except MultipleObjectsReturned:
            return Response({"error":"指定されたプロジェクトが複数存在します。"},status.HTTP_400_BAD_REQUEST)

        except Project.DoesNotExist:
            return Response({"error":"指定されたプロジェクトは存在しません。"},status.HTTP_400_BAD_REQUEST)

        # except Exception as e:
        #     logger.debug(e)
        #     return Response({"error":"指定されたprojectは存在しません"})

        project_serializer = ProjectDeserializer(instance=project_queryset)
        projectJSON = project_serializer.data

        tasklist_queryset_list = TaskList.objects.filter(project=project_queryset)   
        projectData=[]

        
        for tasklist_queryset in tasklist_queryset_list:
            print(tasklist_queryset)
            tasklist_serializer = TaskListSerializer(instance=tasklist_queryset)
            print(tasklist_serializer.data)
            # logger.debug(tasklist_serializer)
            # return Response()

            tasklist = tasklist_serializer.data
            tasklist["tasklist"] = []

            logger.debug(tasklist_queryset)
            task_queryset_list = Task.objects.filter(tasklist=tasklist_queryset)

            for task_queryset in task_queryset_list:
                task_serializer = TaskSerializer(instance=task_queryset)
                tasklist["tasklist"].append(task_serializer.data)

            tasklist["tasklist"] = sorted(tasklist["tasklist"],key=lambda x:x["tasktype"],reverse=True)
            projectData.append(tasklist)

        projectJSON["projectData"] = projectData

        return Response(projectJSON)

            # tasklist=[]
            # task = []

            # task_queryset_list = Task.objects.filter(tasklist=tasklist_queryset)            

            # tasklist_serializer = TaskListSerializer(instance=tasklist_queryset)

             


        
        
         

def get_queryset(self):
 
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        return queryset
        

class ProjectCreateView(generics.GenericAPIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    # permission_classes = [IsAuthenticated,]
    serializer_class = ProjectSerializer
    def post(self,request):
        # test123 = {'project': 'aaaaaaaaaaaaaaaa', 'projectData': [{'tasklist_id': '2d9f9d67-661b-4300-9d17-59097ca4ff93', 'edit': True, 'status': 'waiting', 'tasklist': [{'task': 'サンプルタスク', 'tasktype': 'task'}, {'task': 'サンプルサブタスク', 'tasktype': 'subtask'}]}, {'tasklist_id': '2d9f9d67-661b-4300-9d17-59097ca4ff94', 'edit': True, 'status': 'waiting', 'tasklist': [{'task': 'サンプルタスク', 'tasktype': 'task'}, {'task': 'サンプルサブタスク', 'tasktype': 'subtask'}]}]}

        logger.debug(request.data)

        serializer = self.get_serializer(data=request.data)

        result_valid = serializer.is_valid()
        logger.debug(result_valid)


        if not result_valid:
            logger.debug("308")
            return Response({"OK":False},status=status.HTTP_400_BAD_REQUEST)
        
        logger.debug("")
        created_user = {"created_user":request.user}

        try:
            save = serializer.save(**created_user)
        except Exception:
            return Response({"OK":False},status=status.HTTP_400_BAD_REQUEST)


        return Response({"OK":True},200)

    

        
class TaskCreate(generics.GenericAPIView):
    
    # queryset = TaskModel.objects.all()
    # serializer_class = TaskSerializer　
    authentication_classes = (CookieHandlerJWTAuthentication,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [IsAuthenticated,]
    lookup_field = "created_at"

    def post(self, request):
        # created_at = ""
        # for taskdata in request.data:   
        #     try:
        #         filterd_dict = self.taskdata_validation(taskdata)
        #     except drf_exp.ValidationError:
        #         return Response({"detail": "パラメータが不足しています"}, status=400)
        #     except CustomUser.DoesNotExist:
        #         return Response({"detail": "ユーザーが見つかりませんでした"}, status=400)


        # serializer = TaskSerializer(data=request.data,many=True)
        # serializer.is_valid()
        # print("serializer.data",serializer.data)
        # serializer.save()
        # return Response("test",status=200)


            # try:
            #     created_user = get_object_or_404(CustomUser, email=created_user)
            # except CustomUser.DoesNotExist:
            #     return Response({"error": "ユーザーが見つかりませんでした"}, status=400)
    
            # self.kwargs["created_at"] = self.task_save(filterd_dict)
        
        # self.kwargs["created_at"]=created_at
        # instance = self.get_object()
        # instance = self.get_queryset()
        # serializer = self.get_serializer(instance,many=True)

        
        serializer = self.get_serializer(data=request.data,many=True)
        serializer.is_valid()
        serializer.save()

        
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        # return Response(status=status.HTTP_201_CREATED)


        # print(request.data)

    def taskdata_validation(self,taskdata):
        task_keys = ['task','smalltask','motivation','created_user']
        filterd_dict = self.data_from_dict(taskdata, task_keys)
        
        if None in list(filterd_dict.values()):
            raise drf_exp.ValidationError()

        # if CustomUser.objects.filter(email=filterd_dict["created_user"]).exists():
        #     filterd_dict["created_user"] = CustomUser.objects.get(email=filterd_dict["created_user"])
        # else:
        #     raise CustomUser.DoesNotExist
        

        # try:
        #     filterd_dict["created_user"] = get_object_or_404(CustomUser, email=filterd_dict["created_user"])
        # except CustomUser.DoesNotExist:
        #     raise 
            # return Response({"error": "ユーザーが見つかりませんでした"}, status=400)

        return filterd_dict

    def get_queryset(self,**kwargs):
        queryset = self.queryset
        queryset = queryset.filter(**self.kwargs)

        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        return queryset
  
    def build_dictionary(self,**kwargs):
        tmp_dict = {}
        for k,v in kwargs.items():
            tmp_dict[k] = v
        
        return tmp_dict

    def data_from_dict(self,target_dict,keylist):
        # print(target_dict,"--")
        filterd_dict = {}
        for key in keylist:
            filterd_dict[key] = target_dict.get(key,None)
        
        return filterd_dict
   
    def __task_save(self, taskdata):

        task,smalltask,motivation,created_user = taskdata.values()

        # serializer = TaskSerializer(data=self.build_dictionary(task=task,created_user=created_user))
        task_dict = {}
        task_dict["task"] = task
        # task_dict["task"] = taskdata[""]
        serializer = TaskSerializer(data=task_dict)
        serializer.is_valid(raise_exception=True)
        save_model = serializer.save(created_user=created_user)
        # ここのcreated_userはなぜモデルを指定する必要があるのか？？

        # print(save_model,"save_model")

        # _dict=self.build_dictionary(motivation=request.data['motivation'])

        motivation_dict = {}
        motivation_dict["motivation"] = motivation

        # serializer = MotivationSerializer(data=self.build_dictionary(motivation=motivation))
        serializer = MotivationSerializer(data=motivation_dict)

        # print('otivation',motivation)
        if(serializer.is_valid()):
            # print('is_valid.otivation',motivation)
            serializer.save(task_id=save_model)



      


        for smalltask in smalltask:
            # _dict=self.build_dictionary(smalltask=smalltask['smalltask'])
            smalltask_dict = {}
            smalltask_dict["motivation"] = taskdata["motivation"]

            # serializer = SmallTaskSerializer(data=self.build_dictionary(smalltask=smalltask["smalltask"]))
            serializer = SmallTaskSerializer(data=smalltask_dict)

            if(serializer.is_valid()):
                serializer.save(task_id=save_model)
        
        return save_model.created_at


        # request.data["created_user"]= CustomUser.objects.get(email=request.data["created_user"]).id    
 
            
        # get_user = CustomUser.objects.get(email=created_user)

        # if CustomUser.objects.get(email=created_user).exists():
        #     user = CustomUser.objects.get(email=created_user)
        # else:
            # return Response({"error": "ユーザーが見つかりませんでした"}, status=400)



        
        # task = request.data.get('task',None)
        # smalltask = request.data.get('smalltask',None)
        # motivation = request.data.get('motivation',None)
        # created_user = request.data.get('created_user',None)




        # バリデーション
        # confirm_key_list = ['task','smalltask','motivation','created_user']
        # for confirm_key in confirm_key_list:
        #     if confirm_key not in request.data.keys():
        #         return Response({"error": "パラメータが不足しています"}, status=400)


        # if not (request.data['task'] and request.data['smalltask'] and request.data['motivation'] and request.data['created_user']):
            # return Response({"error": "パラメータが不足しています"}, status=400)

        # request.data['created_user'] = g

        # _dict=self.build_dictionary(task=request.data['task'],created_user=request.data['created_user'])



        # return Response(status=status.HTTP_201_CREATED)
       
class TaskDestroy(DestroyAPIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = [IsAuthenticated,]

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'created_at'

    def delete(self, request, *args, **kwargs):
        created_at = self.request.GET.get("created_at")
        if not created_at:
            # raise ValueError("error!")

            return Response({"error": "パラメータが指定されていません"}, status=400)

        self.kwargs['created_at']=created_at
        return self.destroy(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = Task.objects.filter(**self.kwargs)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)






# class Task(ListAPIView):
#     authentication_classes = (CookieHandlerJWTAuthentication,)
#     permission_classes = [IsAuthenticated,]

#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
    

# class TaskRetrieve(RetrieveAPIView):
#     queryset = TaskModel.objects.all()
#     serializer_class = TaskSerializer 
#     lookup_field = 'task'

# class TaskRetrieve(RetrieveAPIView):
#     authentication_classes = (CookieHandlerJWTAuthentication,)
#     permission_classes = [IsAuthenticated,]
#     queryset = TaskModel.objects.all()
#     serializer_class = TaskSerializer(many=True)
#     lookup_field = 'created_at'


            # tmp_dict = {}
            # tmp_dict['task_id']=save_model.task_id
            # tmp_dict['smalltask']=smalltask['smalltask']

            # print(tmp_dict)



        
        # for motivation in request.data['motivation']:
        # tmp_dict = {}
        # tmp_dict['task_id']=save_model.task_id
        # tmp_dict['motivation']=request.data['motivation']



# createをオーバーライドして泥臭く書く
# task,smalltask,motivationの順で保存し、最後にレスポンスを返す
# class TaskCreate_org(CreateAPIView):
#     queryset = TaskModel.objects.all()
#     serializer_class = TaskSerializer
#     lookup_field = 'task'

#     def create(self, request):

#         serializer = self.get_serializer(data=request.data)
#         # print("serializer:  ",serializer)

#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         print("request.data:",type(serializer.data))
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

        
        #     def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# updateをオーバーライドしてかく
# パラメータのtask_idでtaskを取得→task_idで子モデル取得→子モデルにsetattr
# ってか、編集機能要らなくね？保存ごとに前の日付のデータを消してから保存するから、編集するタイミングないと思う。
# だから実装いらない。
# class TaskUpdate(UpdateAPIView):
#     queryset = TaskModel.objects.all()
#     serializer_class = TaskSerializer
#     lookup_field = 'task'



# 全ての細分化タスクを取得、レスポンスに追加して返す
# class SmallTaskView(APIView):
#     def get(self,request):
#         try:
#             tasks = SmallTask.objects.all()

#             serializer = SmallTaskSerializer(instance=tasks,many=True)

#             return Response({"data":serializer.data},status=status.HTTP_200_OK)

#         except Exception as e:
#             print(e)
#             return Response({"type":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 
# class createdatOfTask(APIView):

#     def get(self, request):

#         # print(request.COOKIES)

#         # print("------",request.META)
#         try:            
#             JWT = request.COOKIES.get("access_token")
#             r = request.COOKIES.get("refresh_token")
            
#             if not JWT:
#                 return Response({"error": "No token"}, status=status.HTTP_401_UNAUTHORIZED)

#             payload = get_object(JWT)
#             rp = get_object(r)

#             now = datetime.now(tz=timezone.utc)
#             print("access_token_exp:",datetime.utcfromtimestamp(payload["exp"]))
#             print("refresh_token_exp:",datetime.utcfromtimestamp(rp["exp"]))
#             print("現在時刻",now)

#             user = CustomUser.objects.get(id=payload["user_id"])
#             tasks = Task.objects.filter(created_user=user)
#             createdat_list = [x.created_at.strftime('%Y-%m-%d') for x in tasks]
#             return Response(createdat_list, status=status.HTTP_200_OK)
#         except Exception as e:
#             print(e)
#             return Response({"type":"error"},status=status.HTTP_200_OK)


#  # RefreshToken取得API
# class TaskView(APIView):
#     def get(self,request):
#         try:
#             created_at = request.GET.get("created_at")
#             tasks = Task.objects.filter(created_at=created_at)
#             serializer = DetailTaskSerializer(instance=tasks,many=True)  
#             return Response(serializer.data,status=status.HTTP_200_OK)

#         except Exception as e:
#             print(e)
#             return Response({"type":"error"},status=status.HTTP_200_OK)

#     def post(self,request):
#         tasks = Task.objects.filter(created_at=request.data["created_at"])
#         deldata = tasks.delete()

#         savetask = ""
#         user = request.data["created_user"]

#         try:
#             print(request.data)
#             print(CustomUser.objects.get(email=user))
#         except Exception as e:
#             print(e)

#         for data in request.data["data"]:
#             task = {"task":data["task"],"created_user":CustomUser.objects.get(email=user).id}
#             serializer = TaskSerializer(data=task)
#             if serializer.is_valid():
#                 savetask = serializer.save()

#             motivation = {"motivation":data["motivation"],"task_id":savetask.task_id}
#             serializer = MotivationSerializer(data=motivation)
#             if serializer.is_valid():
#                 serializer.save()

#             for smalltask in data["smalltask"]:
#                 print(smalltask)
#                 smalltask = {"smalltask":smalltask["smalltask"],"task_id":savetask.task_id}
#                 serializer = SmallTaskSerializer(data=smalltask)
#                 if serializer.is_valid():
#                     serializer.save()
#         return Response(status=status.HTTP_200_OK)

#     def delete(self,request):
#         tasks = Task.objects.filter(created_at=request.data["created_at"])
#         deldata = tasks.delete()
#         print(deldata)
#         # serializer =TaskSerializer(instance=tasks,many=True)
        
#         return Response({"type":"success"},status=status.HTTP_200_OK)

# class SmallTaskViewSet(viewsets.ModelViewSet):
#     queryset = SmallTask.objects.all()
#     serializer_class = SmallTaskSerializer

