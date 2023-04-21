import jwt

from Todo_DRF_app.models import CustomUser,Task,TaskList,Project
from jwt.exceptions import DecodeError
from rest_framework import status
from rest_framework.exceptions import NotFound,APIException
from Todo_DRF.settings import settings_dev as settings


def create_user(**kwargs):
    return CustomUser.objects.create(**kwargs)

def create_task(**kwargs):
    return Task.objects.create(**kwargs)

def create_url(url,**kwargs):
    query = ""
    for i,dict_v in enumerate(list(kwargs.items())):
        query += "?" if i == 0 else "&"
        query += str(dict_v[0])+"="+str(dict_v[1])
    url += query
    return url

def set_token(request,token):    
    request.COOKIES["access_token"] = str(token.access_token)
    request.COOKIES["refresh_token"] = str(token)

    return request

def verify_jwt(JWT):
        try:
            jwt.decode(jwt=str(JWT), key=settings.SECRET_KEY, algorithms=["HS256"],)
            return True
        except DecodeError as e:
            # APIExceptionをraiseすると自動的にHTTPレスポンスを作り返す仕組み
            return False



# def send_request(view,request,cookie=None):
#     # for key,value in cookie.items():
#     if cookie:
#         request.COOKIES["access_token"] = cookie["access"]
#     return view(request)