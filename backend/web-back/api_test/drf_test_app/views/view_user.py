from rest_framework.generics import DestroyAPIView,UpdateAPIView,ListAPIView,RetrieveAPIView,CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from ..authentication import CookieHandlerJWTAuthentication
from ..serialyzer import UserSerializer
from ..models import CustomUser
import json

# import base64

# def base64decode(encodetext):
#     textBytes = base64.b64decode(encodetext.encode())
#     return textBytes.decode()

# class User(ListAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer

class UserRetrieve(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        userid = request.GET.get("userid")
        
        if not userid:
            return Response({"detail": "ユーザIDが指定されていません"}, status=400)

        self.kwargs["id"] = userid
        
        return self.retrieve(request, *args, **kwargs)

        # raise MethodNotAllowed('GET')

    # def post(self,request, *args,**kwargs):
    #     # url_params = self.request.GET.get("email")

    #     bytes_body = request.body

    #     try:
    #         json_body = json.loads(bytes_body)
    #     except json.JSONDecodeError:
    #         return Response({"error": "パラメータの形式が間違っています"}, status=400)

    #     if "email" not in json_body:
    #         return Response({"error": "パラメータの指定が間違っています"}, status=400)
            
    #     self.kwargs['email']=json_body["email"]

    #     return self.retrieve(request, *args, **kwargs)


    # def get(self, request, *args, **kwargs):

    #     url_params = self.request.GET.get("email")
    #     if not url_params:
    #         return Response({"error": "パラメータが指定されていません"}, status=400)
    
    #     self.kwargs['email']=base64decode(url_params)
    #     return self.retrieve(request, *args, **kwargs)

class UserCreate(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'

    def post(self, request, *args, **kwargs):
        # print("request.POST:    ",self.request.body)
        # bytes_body = request.body
        # json_body = json.loads(bytes_body)

        # print("json_data:",json_body["email"])
        kwargs["password"] = request.data.pop('password', None)
        if kwargs["password"] == None:
            return Response({"detail": "パスワードが指定されていません"}, status=400)
            
        # json_body["password"]

        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # bytes_body = request.body
        # json_body = json.loads(bytes_body)

        # print("json_data:",json_body["email"])
        # print("serializer.validated_dat",serializer.validated_data)

        # print("request.body:   ",request,kwargs,args)
        
        if kwargs["password"]:
            serializer.validated_data["password"] = kwargs["password"]
        
        # print("serializer.validated_data",serializer.validated_data)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserUpdate(UpdateAPIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = [IsAuthenticated,]

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        # print(kwargs,args)
        # print("request.data: ",request.data)
        userid = self.request.GET.get("userid")
       
        if not userid:
            return Response({"detail": "ユーザIDが指定されていません"}, status=400)

        self.kwargs["id"] = userid

            
        # bytes_body = request.body

        # return Response({"error": "パラメータの形式が間違っています"}, status=200)


        # try:
        #     json_body = json.loads(bytes_body)
        # except json.JSONDecodeError:
        #     return Response({"error": "パラメータの形式が間違っています"}, status=400)

        

        # updateuser = json_body.pop('updateuser', None)

        # if not updateuser:
        #     return Response({"error": "更新するユーザーが取得できませんでした"}, status=400)

        kwargs["password"] = request.data.pop('password', None)

        # if kwargs["password"] == None:
        #     return Response({"error": "パスワードが指定されていません"}, status=400)
    

        # url_params = self.request.GET.get("email")
        
        # self.kwargs['email']=self.request.user
        # base64decode(url_params)
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["password"] = kwargs["password"]

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)


    # put メソッドをオーバーライド
    # トークンからuser取得

class UserDestroy(DestroyAPIView):
    authentication_classes = (CookieHandlerJWTAuthentication,)
    permission_classes = [IsAuthenticated,]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        userid = request.GET.get("userid")
      
        if not userid:
            return Response({"detail": "ユーザIDが指定されていません"}, status=400)

        self.kwargs["id"] = userid
        return self.destroy(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        bytes_body = request.body

        try:
            json_body = json.loads(bytes_body)
        except json.JSONDecodeError:
            return Response({"detail": "パラメータの形式が間違っています"}, status=400)

        destoryuser = json_body.pop('destoryuser', None)

        if not destoryuser:
            return Response({"detail": "削除するユーザーが取得できませんでした"}, status=400)


        # url_params = self.request.GET.get("email")
        # if not url_params:
        #     return Response({"error": "パラメータが指定されていません"}, status=400)

        self.kwargs['email']=destoryuser
        # base64decode(url_params)
        return self.destroy(request, *args, **kwargs)

# ユーザー退会API
# class UserDeactivate(APIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             instance = CustomUser.objects.get(email=request.data["email"])
#             serializer = UserSerializer(instance=instance,data={"active":0},partial=True)

#             if serializer.is_valid():
#                 username = serializer.save()

#             return Response({"username":username},status=status.HTTP_200_OK)

#         except Exception as e:
#             print(e)
#             return Response({"error":"エラー発生"},status=status.HTTP_400_BAD_REQUEST)

#         return Response({"data":"","type":"error"},status=status.HTTP_200_OK)



# ユーザー登録API
# class UserRegisterView(APIView):
#     def post(self, request, *args, **kwargs):
        

#         try:
#             response = Response()
#             newuser = RegisterUserSerializer(data=request.data)
#             if newuser.is_valid():
#                 user = newuser.save()
#                 print(user)
#                 response.data=user

#                 return response

#         except Exception as e:
#             print(e)
#             return Response({"type":"error"},status=status.HTTP_400_BAD_REQUEST)


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