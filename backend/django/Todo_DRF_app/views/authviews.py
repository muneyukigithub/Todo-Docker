from rest_framework_simplejwt import views as jwt_views
from rest_framework.response import Response
from rest_framework.exceptions import NotFound,APIException
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from ..authentication import CookieHandlerJWTAuthentication
from Todo_DRF.settings import settings_dev as settings
from django.shortcuts import get_object_or_404
from ..models import Task,CustomUser
from ..serialyzer import UserSerializer
from .utils import get_payload
from logging import getLogger,config
config.dictConfig(settings.LOGGING)
logger = getLogger(__name__)


# JWTトークンからUser名を抽出して返すAPI
class JWTUserInfo(RetrieveAPIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = [IsAuthenticated,]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_object(self):
        access_token = self.request.COOKIES.get('access_token')

        payload = get_payload(access_token)

        user_id = payload.get('user_id')

        self.kwargs[self.lookup_field] = user_id

        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

# JWTトークン発行API
class JWTCreateToken(jwt_views.TokenObtainPairView):

    def createJWTResponse(self,request):
        response = super().post(request)
        response.set_cookie(
            "access_token",
            response.data['access'],
            max_age=60 * 60 * 24,
            httponly=True,
            samesite="None",
            secure=True,)

        response.set_cookie(
            "refresh_token",
            response.data['refresh'],
            max_age=60 * 60 * 24 * 30,
            httponly=True,
            samesite="None",
            secure=True,)


        return response


    def post(self, request, *args, **kwargs):
        return self.createJWTResponse(request=request)



# JWTトークン削除API
class JWTDestroyToken(jwt_views.TokenObtainPairView):
    def createJWTResponse(self):
        response = Response("削除ok",status=status.HTTP_204_NO_CONTENT)

        response.delete_cookie('access_token',samesite='None')
        response.delete_cookie('refresh_token',samesite='None')
        return response
 
    def get(self,request,*args,**kwargs):
        return self.createJWTResponse()


# JWTトークン削除リフレッシュAPI
class JWTRefresh(jwt_views.TokenRefreshView):
    def refresh_token_response(self,request):

        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            raise InvalidToken(detail="リフレッシュトークンが指定されていません")

        serializer = self.get_serializer(data={'refresh':refresh_token})

        # 失敗したらInvalidToken例外
        # InvalidTokenはAPIExceptionを継承しているためこれだけでいい
        serializer.is_valid(raise_exception=True)

        response = Response(data=serializer.validated_data,status=status.HTTP_200_OK)

        response.set_cookie(
        "access_token",
        serializer.validated_data["access"],
        max_age=60 * 60 * 24,
        httponly=True,
        samesite="None",
        secure=True,)

        return response

    def get(self,request):
        return self.refresh_token_response(request)

# JWTトークン検証API
class JWTVerifyAccessTokenView(APIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def verify_jwt(self,request):
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            raise NotFound(detail="アクセストークンが指定されていません")

        try:
            get_payload(access_token)
            return Response({"message": "JWT検証OK"}, status=status.HTTP_200_OK)
        except APIException:
            return Response({"message":"JWT検証NG"},status=status.HTTP_401_UNAUTHORIZED)

    def get(self,request):
        return self.verify_jwt(request)
  