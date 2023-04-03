# from django.shortcuts import render
# from rest_framework import viewsets
from ..models import Task,CustomUser
from ..serialyzer import (
    TaskSerializer,
    UserSerializer,

)

from rest_framework_simplejwt import views as jwt_views
# from rest_framework_simplejwt import exceptions as jwt_exp
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
import jwt
from django.conf import settings
# from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..authentication import CookieHandlerJWTAuthentication
# from .authentication import CookieHandlerJWTAuthentication
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.shortcuts import get_object_or_404
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from datetime import datetime,timezone
# import time

from logging import getLogger,config
config.dictConfig(settings.LOGGING)
logger = getLogger(__name__)


# tokenをbase64デコードして、User名を返すAPI
class jwt_userinfo(APIView):
    # authentication_classes = [JWTAuthentication,]
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        
        return_user = {}
        return_user["username"] = "guest"
    
        JWT = request.COOKIES.get("access_token")

        # if not JWT:
        #     return Response({"error": "No token"}, status=400)

        try:
            payload = get_object(JWT)
        except Exception as e:
            print(e)
            return Response({"error": "jwt decode failed"}, status=401)


        user = CustomUser.objects.get(id=payload["user_id"])
        if user:
            seriallizer = UserSerializer(user)
            return_user['username'] = seriallizer.data['email']
            
        return Response(return_user, status=200)

    # RefreshToken取得API


# ログインAPI(JWTTokenを発行してレスポンスのcookieに追加)
class jwt_createtoken(jwt_views.TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        logger.debug(request.data)

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
        

# トークン削除(レスポンスに有効期限が0のJWTをcookieにセットして返す)
class jwt_destroytoken(jwt_views.TokenObtainPairView):
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


class jwt_refresh(jwt_views.TokenRefreshView):
    # authentication_classes = (CookieHandlerJWTAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        response = Response()

        JWT = request.COOKIES.get('refresh_token')
        print(JWT,"refresh\n")
        if not JWT:
            return Response({"error": "No token"}, status=401)
        
        # refreshToken = {"refresh": request.COOKIES["refresh_token"]}
        # request.COOKIES["refresh_token"]
        refresh_token = {}
        refresh_token['refresh'] =  JWT
        serializer = self.get_serializer(data=refresh_token)

        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            # raise jwt_exp.InvalidToken(e.args[0])
            print(e)
            return Response({"error": "jwt decode failed"}, status=401)

        # print(serializer.validated_data,"-------------")

        response.set_cookie(
        "access_token",
        serializer.validated_data["access"],
        max_age=60 * 60 * 24,
        httponly=True,
        samesite="None",
        secure=True,)

        # response.set_cookie(
        # "refresh_token",
        # serializer.validated_data["refresh"],
        # max_age=60 * 60 * 24 * 30,
        # httponly=True,
        # samesite="None",
        # secure=True,)

        # refresh_token['refresh'] = serializer.validated_data["access"]

        return_token = {}
        return_token['access_token'] = serializer.validated_data["access"]
        return_token['refresh'] = JWT
        response.data=return_token
        response.status_code=200
        print("\nrefresh OK\n")


        return response

# RefreshToken取得API
# def jwt_refreshtoken(request):
#     authentication_classes = (CookieHandlerJWTAuthentication,)
#     permission_classes = (IsAuthenticated,)


#     try:
#         refresh_token = {}
#         refresh_token['refresh'] = request.COOKIES.get("refresh_token")

#         return Response(refresh_token, status=status.HTTP_200_OK)
#     except Exception as e:
#         print(e)
#         return Response({"error": "refreshtoken not found"}, status=400)



class jwt_verifyaccesstoken(APIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        
      
        accessToken = request.COOKIES.get("access_token")
        print(accessToken)

        try:
            get_object(accessToken)
        except:
            print("verify NG")
            return Response({"message":"JWT検証NG"},status=status.HTTP_401_UNAUTHORIZED)

        print("verify OK")
        return Response({"message": "JWT検証OK"}, status=status.HTTP_200_OK)

class jwt_verifyrefreshtoken(APIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get(self,request):
        refreshToken = request.COOKIES.get("refresh_token")

        try:
            get_object(refreshToken)
        except:
            print("verify NG")
            return Response({"message":"JWT検証NG"},status=status.HTTP_401_UNAUTHORIZED)

        print("verify OK")
        return Response({"message": "JWT検証OK"}, status=status.HTTP_200_OK)


def get_object(JWT):
        try:
            payload = jwt.decode(jwt=JWT, key=settings.SECRET_KEY, algorithms=["HS256"],)

            return payload

        except Exception as e:
            print(e)  
            raise Exception(e)

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