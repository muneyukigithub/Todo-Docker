# settings_devは開発環境用

from .settings import * 
from .settings_local import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 
ALLOWED_HOSTS = ["*"]

# CookieのSameSite属性の設定
# Noneで、オリジン間でCookieの送信が可能
SESSION_COOKIE_SAMESITE = None

# CookieのSecure属性の設定
# TrueでHTTPSのみでCookieの送信が可能
SESSION_COOKIE_SECURE = True

# CORSで許可するオリジンのリスト
# CORS_ORIGIN_WHITELIST = []

# CORSで全てのオリジンからのアクセスを許可
CORS_ALLOW_ALL_ORIGINS = True

# オリジン間でCookieを送信するための設定
CORS_ALLOW_CREDENTIALS = True

# CSRF保護において、リクエストを許可するオリジンのリスト
CSRF_TRUSTED_ORIGINS = ["localhost", "127.0.0.1"]

# DB設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # mysqlを指定
        'NAME': 'TodoListDB', # 開発用データベース名
        'USER': 'root', # 開発用ユーザー名
        'PASSWORD': 'password', # 開発用パスワード
        'HOST': 'db',# Dockerのサービス名
        'PORT': '3306',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }