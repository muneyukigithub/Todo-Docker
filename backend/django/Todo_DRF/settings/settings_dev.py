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
CORS_ORIGIN_ALLOW_ALL = True


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
        'USER': 'user', # 開発用ユーザー名
        'PASSWORD': 'password', # 開発用パスワード
        'HOST': 'db',# Dockerのサービス名
        'PORT': '3306',
    }
}




LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s a',
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
