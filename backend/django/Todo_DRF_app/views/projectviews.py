from logging import config, getLogger
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import exceptions as drf_exp
from rest_framework import generics, status, viewsets
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import exceptions as jwt_exp
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from Todo_DRF.settings import settings_dev as settings
from ..authentication import CookieHandlerJWTAuthentication
from ..models import CustomUser, Project, Task, TaskList
from ..serialyzer import (ProjectDeserializer, ProjectSerializer
                          )

config.dictConfig(settings.LOGGING)
logger = getLogger(__name__)

# プロジェクト情報を返すAPI
class ProjectView(generics.RetrieveAPIView):
    # serializer_class = ProjectDeserializer
    serializer_class = ProjectDeserializer
    queryset = Project.objects.all()
    lookup_field = 'project'

    def retrieve(self, request, *args, **kwargs):
        self.kwargs[self.lookup_field] = request.GET.get("project")
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# 全プロジェクト情報を返すAPI
class ProjectListView(generics.ListAPIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = [IsAuthenticated,]
    serializer_class = ProjectDeserializer
    queryset = Project.objects.all()

    def get_queryset(self):
        queryset = self.queryset.all().filter(created_user=self.request.user)
        return queryset


# プロジェクト情報を作成するAPI
class ProjectCreateView(generics.GenericAPIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = [IsAuthenticated,]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        save = serializer.save(**{"created_user":request.user})

        return Response({"detail":"プロジェクトの保存が完了しました。"},status=status.HTTP_201_CREATED)

# プロジェクト情報を削除するAPI
class ProjectDeleteView(generics.DestroyAPIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = [IsAuthenticated,]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'project'

    def delete(self, request, *args, **kwargs):
        project = request.GET.get("project")

        if not project:
            return Response({"detail":"プロジェクト名が指定されていません。"},400)

        self.kwargs[self.lookup_field] = project
        return self.destroy(request, *args, **kwargs)

