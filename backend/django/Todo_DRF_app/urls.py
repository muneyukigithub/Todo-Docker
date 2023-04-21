from django.urls import path, include
from rest_framework import routers
from .views.userviews import UserDestroy,UserCreate,UserRetrieve
from .views.projectviews import ProjectCreateView,ProjectView,ProjectListView,ProjectDeleteView
router = routers.DefaultRouter()
from .views.authviews import *
urlpatterns = [

    # プロジェクト
    path("project/",ProjectView.as_view()),
    path("projectlist/",ProjectListView.as_view()),
    path("projectcreate/",ProjectCreateView.as_view()),
    path("projectdelete/",ProjectDeleteView.as_view()),
    
    # ユーザー
    path("user/",UserRetrieve.as_view()),
    path("usercreate/",UserCreate.as_view()),
    path("userdelete/",UserDestroy.as_view()),

    # 認証
    path("jwt_userinfo/",JWTUserInfo.as_view()),
    path("jwt_createtoken/",JWTCreateToken.as_view()),
    path("jwt_deletetoken/",JWTDestroyToken.as_view()),
    path("jwt_refresh/",JWTRefresh.as_view()),
    path("jwt_verifyaccesstoken/",JWTVerifyAccessTokenView.as_view()),
   ]

