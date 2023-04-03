from django.shortcuts import render
from rest_framework import viewsets
from .models import Task, SmallTask, CustomUser
from .serialyzer import (
    TaskSerializer,
    SmallTaskSerializer,
    UserSerializer,
    RegisterUserSerializer,
    DetailTaskSerializer,
    MotivationSerializer
)
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt import exceptions as jwt_exp
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
import jwt
from django.conf import settings
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from .authentication import CookieHandlerJWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime,timezone
import time


# ユーザー退会API
class UserDeactivate(APIView):
    def post(self, request, *args, **kwargs):
        try:
            instance = CustomUser.objects.get(email=request.data["email"])
            serializer = UserSerializer(instance=instance,data={"active":1},partial=True)

            if serializer.is_valid():
                username = serializer.save()
                print(username)
            return Response({"data":{"username":""},"type":"success"},status=status.HTTP_200_OK)

        except Exception as e:
            pass

        return Response({"data":"","type":"error"},status=status.HTTP_200_OK)

# ユーザー登録API
class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        

        try:
            response = Response()
            newuser = RegisterUserSerializer(data=request.data)
            if newuser.is_valid():
                user = newuser.save()
     
                response.data=user

                # token = TokenObtainPairSerializer.get_token(user)
                # response.set_cookie(
                #         "access_token",
                #         # newtoken.validated_data["access"],
                #         str(token.access_token),
                #         max_age=60 * 60 * 24,
                #         httponly=True,
                #         samesite="None",
                #         secure=True,
                #     )
                # response.set_cookie(
                #         "refresh_token",
                #         # newtoken.validated_data["refresh"],
                #         str(token),
                #         max_age=60 * 60 * 24 * 30,
                #         httponly=True,
                #         samesite="None",
                #         secure=True,
                #     )

                # response.data = {"type":"success","access_token":str(token.access_token),"refresh":str(token)}
                # response.status_code = 200
                return response

        except Exception as e:
            print(e)
            return Response({"type":"error"},status=status.HTTP_400_BAD_REQUEST)




def get_object(JWT):
        try:
            payload = jwt.decode(jwt=JWT, key=settings.SECRET_KEY, algorithms=["HS256"])

            return payload

        except Exception as e:

            print("get_object error !!!")
            
            raise Exception(e)

# 全ての細分化タスクを取得、レスポンスに追加して返す
class SmallTaskView(APIView):
    def get(self,request):
        try:
            tasks = SmallTask.objects.all()

            serializer = SmallTaskSerializer(instance=tasks,many=True)

            return Response({"data":serializer.data},status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"type":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 
class createdatOfTask(APIView):

    def get(self, request):

        # print(request.COOKIES)

        # print("------",request.META)
        try:            
            JWT = request.COOKIES.get("access_token")
            r = request.COOKIES.get("refresh_token")
            



            # print(JWT)
            # print(request.COOKIES)
            

            if not JWT:
                return Response({"error": "No token"}, status=status.HTTP_401_UNAUTHORIZED)

            payload = get_object(JWT)
            rp = get_object(r)

            now = datetime.now(tz=timezone.utc)
            print("access_token_exp:",datetime.utcfromtimestamp(payload["exp"]))
            print("refresh_token_exp:",datetime.utcfromtimestamp(rp["exp"]))
            print("現在時刻",now)

            user = CustomUser.objects.get(id=payload["user_id"])
            tasks = Task.objects.filter(created_user=user)
            createdat_list = [x.created_at.strftime('%Y-%m-%d') for x in tasks]
            return Response(createdat_list, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"type":"error"},status=status.HTTP_200_OK)


 # RefreshToken取得API
class TaskView(APIView):
    def get(self,request):
        try:
            created_at = request.GET.get("created_at")
            tasks = Task.objects.filter(created_at=created_at)
            serializer = DetailTaskSerializer(instance=tasks,many=True)  
            return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"type":"error"},status=status.HTTP_200_OK)

    def post(self,request):
        tasks = Task.objects.filter(created_at=request.data["created_at"])
        deldata = tasks.delete()

        savetask = ""
        user = request.data["created_user"]

        try:
            print(request.data)
            print(CustomUser.objects.get(email=user))
        except Exception as e:
            print(e)

        for data in request.data["data"]:
            task = {"task":data["task"],"created_user":CustomUser.objects.get(email=user).id}
            serializer = TaskSerializer(data=task)
            if serializer.is_valid():
                savetask = serializer.save()

            motivation = {"motivation":data["motivation"],"task_id":savetask.task_id}
            serializer = MotivationSerializer(data=motivation)
            if serializer.is_valid():
                serializer.save()

            for smalltask in data["smalltask"]:
                print(smalltask)
                smalltask = {"smalltask":smalltask["smalltask"],"task_id":savetask.task_id}
                serializer = SmallTaskSerializer(data=smalltask)
                if serializer.is_valid():
                    serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self,request):
        tasks = Task.objects.filter(created_at=request.data["created_at"])
        deldata = tasks.delete()
        print(deldata)
        # serializer =TaskSerializer(instance=tasks,many=True)
        
        return Response({"type":"success"},status=status.HTTP_200_OK)

# class SmallTaskViewSet(viewsets.ModelViewSet):
#     queryset = SmallTask.objects.all()
#     serializer_class = SmallTaskSerializer


# ログインAPI(JWTTokenを発行してレスポンスのcookieに追加)
class TokenObtainView(jwt_views.TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        # print(request.user)
        # print(request.auth)


        try:
            response = Response()
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            response.set_cookie(
            "access_token",
            serializer.validated_data["access"],
            max_age=60 * 60 * 24,
            httponly=True,
            samesite="None",
            secure=True,)

            response.set_cookie(
            "refresh_token",
            serializer.validated_data["refresh"],
            max_age=60 * 60 * 24 * 30,
            httponly=True,
            samesite="None",
            secure=True,)

            response.data=serializer.validated_data
            response.status_code=200

            return response

        except Exception as e:
            print(e)
            return Response({"message": "認証エラーにより失敗"}, status=401)
        

# TokenからUser取得するAPI
class UserAPIView(APIView):

    def get(self, request, format=None):

        # print(request.COOKIES)
        JWT = request.COOKIES.get("access_token")
        if not JWT:
            return Response({"error": "No token"}, status=400)

        payload = get_object(JWT)
        # print(payload["exp"])
        user = CustomUser.objects.get(id=payload["user_id"])

        serial = UserSerializer(user)
        # return Response({"error": "No token"}, status=200)

        return Response({"username": serial.data["email"]}, status=200)

    # RefreshToken取得API


def refresh_get(request):

    try:
        rt = request.COOKIES["refresh_token"]
        return JsonResponse({"refresh": rt}, safe=False)
    except Exception as e:
        print(e)

    return None

    # RefreshToken取得API


import json


class TokenRefresh(jwt_views.TokenRefreshView):
    def get(self, request, *args, **kwargs):
        response = Response()
        refreshToken = {"refresh": request.COOKIES["refresh_token"]}
        # request.COOKIES["refresh_token"]
        serializer = self.get_serializer(data=refreshToken)
        try:
            serializer.is_valid(raise_exception=True)
        except jwt_exp.TokenError as e:
            raise jwt_exp.InvalidToken(e.args[0])
        response.set_cookie(
            "access_token",
            serializer.validated_data["access"],
            max_age=60 * 24 * 24 * 30,
            httponly=True,
            samesite="None",
            secure=True,
        )

        return response


        # print("---------request.data")
        # print(request.data)
        # print(type(request.data))
        # nowtoken = {"refresh": request.COOKIES["refresh_token"]}
        # print(type(nowtoken))
        # print(json.dumps(nowtoken))
        # # serializer = self.get_serializer(data=request.data)
        # serializer = self.get_serializer(data=nowtoken)
        # try:
        #     serializer.is_valid(raise_exception=True)
        # except jwt_exp.TokenError as e:
        #     raise jwt_exp.InvalidToken(e.args[0])
        # # token更新
        # res = Response(serializer.validated_data, status=200)
        # # 既存のAccess_Tokenを削除
        # res.delete_cookie("access_token")
        # # 更新したTokenをセット
        # res.set_cookie(
        #     "access_token",
        #     serializer.validated_data["access"],
        #     max_age=60 * 24 * 24 * 30,
        #     httponly=True,
        #     samesite="None",
        #     secure=True,
        # )
        # return res

    # Token削除API

class verifyAccessToken(APIView):
    def get(self,request):
        accessToken = request.COOKIES["access_token"]

        try:
            get_object(accessToken)
        except:
            print("verify NG")
            return Response({"message":"JWT検証NG"},status=status.HTTP_401_UNAUTHORIZED)

        print("verify OK")
        return Response({"message": "JWT検証OK"}, status=200)

class verifyRefreshToken(APIView):

    def get(self,request):
        refreshToken = request.COOKIES["refresh_token"]

        try:
            get_object(refreshToken)
        except:
            print("verify NG")
            return Response({"message":"JWT検証NG"},status=status.HTTP_401_UNAUTHORIZED)

        print("verify OK")
        return Response({"message": "JWT検証OK"}, status=200)

# ログアウト(レスポンスに有効期限が0のJWTをcookieにセットして返す)
class LogoutView(jwt_views.TokenObtainPairView):
    # authentication_classes = (CookieHandlerJWTAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        res = Response({"message": "logout"}, status=200)
        res.set_cookie(
            "access_token",
            "",
            max_age=0,
            httponly=True,
            samesite="None",
            secure=True,
        )
        res.set_cookie(
            "refresh_token",
            "",
            max_age=0,
            httponly=True,
            samesite="None",
            secure=True,
        )

        return res
