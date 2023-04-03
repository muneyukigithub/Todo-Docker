from ..models import CustomUser
from ..models import Task

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
    request.COOKIES["access_token"] = token["access"]
    request.COOKIES["refresh_token"] = token["refresh"]

    return request



# def send_request(view,request,cookie=None):
#     # for key,value in cookie.items():
#     if cookie:
#         request.COOKIES["access_token"] = cookie["access"]
#     return view(request)