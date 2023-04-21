import json
from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..authentication import CookieHandlerJWTAuthentication
from ..models import CustomUser
from ..serialyzer import UserSerializer
from Todo_DRF.settings import settings_dev as settings

from logging import getLogger,config
config.dictConfig(settings.LOGGING)
logger = getLogger(__name__)

# ユーザー情報を返すAPI
class UserRetrieve(RetrieveAPIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = [IsAuthenticated,]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        userid = request.GET.get("userid")
        if not userid:
            return Response({"detail": "ユーザIDが指定されていません"}, status=status.HTTP_400_BAD_REQUEST)
        
        self.kwargs[self.lookup_field] = userid
        return self.retrieve(request, *args, **kwargs)

# ユーザー情報を作成するAPI
class UserCreate(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        logger.debug(("request.data:",request.data))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        password = serializer.validated_data.get('password')
        password2 = self.request.data.get('password2')
        if password != password2:
            logger.error("password1 password2 miss match")
            raise serializers.ValidationError("パスワードが一致しません")
        serializer.save()


# ユーザー情報を削除するAPI
class UserDestroy(DestroyAPIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = [IsAuthenticated,]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        userid = request.GET.get("userid")
      
        if not userid:
            return Response({"ok":False,"message": "ユーザIDが指定されていません"}, status=400)

        logger.debug((request.user.id,userid))

        if request.user.id != int(userid):
            return Response({"ok":False,"message": "削除不可能なユーザーが指定されました"}, status=400)


        self.kwargs["id"] = userid
        return self.destroy(request, *args, **kwargs)


# ユーザー情報を更新するAPI
# class UserUpdate(UpdateAPIView):
#     authentication_classes = (CookieHandlerJWTAuthentication,)
#     permission_classes = [IsAuthenticated,]

#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = 'id'

#     def put(self, request, *args, **kwargs):

#         userid = self.request.GET.get("userid")
       
#         if not userid:
#             return Response({"detail": "ユーザIDが指定されていません"}, status=400)

#         self.kwargs["id"] = userid


#         kwargs["password"] = request.data.pop('password', None)

#         return self.update(request, *args, **kwargs)

#     def update(self, request, *args, **kwargs):

#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data["password"] = kwargs["password"]

#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):

#             instance._prefetched_objects_cache = {}

#         return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)
