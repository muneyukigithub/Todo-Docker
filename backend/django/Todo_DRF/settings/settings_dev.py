from .settings import * 
from .settings_local import *

# 開発環境の場合はTrue
DEBUG = True

# サービスを提供するドメインの設定
ALLOWED_HOSTS = ["localhost","127.0.0.1"]

# CookieのSameSite属性の設定
# Noneで、オリジン間でCookieの送信が可能
SESSION_COOKIE_SAMESITE = None

# CookieのSecure属性の設定
# TrueでHTTPSのみでCookieの送信が可能
SESSION_COOKIE_SECURE = False

# CORSで許可するオリジンのリスト
# Access-Control-Allow-Originヘッダーがレスポンスに付与される
CORS_ORIGIN_WHITELIST = ["http://localhost","http://127.0.0.1"]

# CORSで全てのオリジンからのアクセスを許可
# CORS_ALLOW_ALL_ORIGINS = True

# オリジン間でCookieを送信するための設定
# Access-Control-Allow-Credentialsヘッダーがレスポンスに付与される
CORS_ALLOW_CREDENTIALS = True

# CSRF保護において、リクエストを許可するオリジンのリスト
CSRF_TRUSTED_ORIGINS = ["localhost", "127.0.0.1"]

# DB設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 変更
        'NAME': 'TodoListDB', # プロジェクトで使用するデータベース名
        'USER': 'root', # パソコンにインストールしたMySQLのユーザー名
        'PASSWORD': 'password', # 同上。そのパスワード
        'HOST': 'db',
        'PORT': '3306',
    }
}

