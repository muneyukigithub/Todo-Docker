from django.urls import path, include
from rest_framework import routers
from .views.view_user import UserDestroy,UserCreate,UserRetrieve,UserUpdate
from .views.view_task import ProjectCreateView,ProjectView,ProjectListView
router = routers.DefaultRouter()

from .views.view_auth import jwt_userinfo,jwt_createtoken,jwt_destroytoken,jwt_refresh,jwt_verifyaccesstoken,jwt_verifyrefreshtoken

urlpatterns = [
    path("projectlist/",ProjectListView.as_view()),
    path("project/",ProjectView.as_view()),
    path("createproject/",ProjectCreateView.as_view()),

    # path("task_filtered_createdat/<str:created_at>/",task_filtered_createdat.as_view()),

    # path("task/",Task.as_view()),
    # path("task_retrieve/<str:task>/",TaskRetrieve.as_view()),
    # path("task_create/",TaskCreate.as_view()),
    # path("task_update/<str:task>/",TaskUpdate.as_view()),
    # path("task_destory/<str:task>/",TaskDestroy.as_view()),

    # 全てのユーザー情報を取得する機会はないので不要
    # path("user/",User.as_view()),

    
    # path("user_retrieve/<str:email>/",UserRetrieve.as_view()),
    # プロフィール情報を取得する際に使う
    path("user/",UserRetrieve.as_view()),

    # ユーザー登録で使う
    path("usercreate/",UserCreate.as_view()),

    # path("user_update/<str:email>/",UserUpdate.as_view()),
    # ユーザー名前変更で使う
    path("userupdate/",UserUpdate.as_view()),
    
    # ユーザー削除で使う
    path("userdelete/",UserDestroy.as_view()),

    # path("user_update/<str:email>/",UserUpdate.as_view()),
    # path("user_destory/<str:email>/",UserDestroy.as_view()),]

    # path("task/",TaskList.as_view()),

    # path("taskretrieve/",TaskRetrieve.as_view()),

    # path("task_retrieve/<str:created_at>/",TaskRetrieve.as_view()),
    # path("taskcreate/",TaskCreate.as_view()),
    # path("task_destory/<str:created_at>/",TaskDestroy.as_view()),
    # path("taskdelete/",TaskDestroy.as_view()),



    path("jwt_userinfo/",jwt_userinfo.as_view()),
    path("jwt_createtoken/",jwt_createtoken.as_view()),
    path("jwt_deletetoken/",jwt_destroytoken.as_view()),
    path("jwt_refresh/",jwt_refresh.as_view()),
    # path("jwt_refreshtoken/",jwt_refreshtoken),
    path("jwt_verifyaccesstoken/",jwt_verifyaccesstoken.as_view()),
    path("jwt_verifyrefreshtoken/",jwt_verifyrefreshtoken.as_view()),

    # userinfo 送信したユーザー情報と、レスポンスのユーザー情報が同じこと
    # createtoken トークン発行していないとき、userinfo失敗。発酵後は成功


    # # タスク取得
    # path("task/",TaskView.as_view(),name="task"),

    # # 細分化タスク取得
    # path("smalltask/",SmallTaskView.as_view(),name="task"),

    # # 保存タスクのcreated_at取得
    # path("savetask_createdat/",createdatOfTask.as_view(),name="task"),
    
    # # ユーザー登録
    # path("userRegist/", UserRegisterView.as_view(), name="userRegist"),

    # # トークンリフレッシュ
    # path("tokenRefresh/", TokenRefresh.as_view(), name="TokenRefresh"),

    # # リフレッシュトークン取得
    # path("refreshToken/", refresh_get,name="refreshToken"),

    # # ユーザー情報取得
    # path("user/", UserAPIView.as_view(), name="UserAPIView"),

    # # ログイン
    # path("token/",views.TokenObtainView.as_view(),name="TokenObtainView"),

    # # ログアウト
    # path("logout/", LogoutView.as_view(), name="LogoutView"),

    # # ユーザー退会
    # path("UserDeactivate/",UserDeactivate.as_view(),name="UserDeactivate"),   

    # path("verifyAccessToken/",verifyAccessToken.as_view()),
    # path("verifyRefreshToken/",verifyRefreshToken.as_view()),
    # # path("verifyRefreshToken/",verifyRefreshToken.as_view()),
    
    
   ]

