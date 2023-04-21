from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.conf import settings

from logging import getLogger,config
config.dictConfig(settings.LOGGING)
logger = getLogger(__name__)



# JWTトークンを使用して認証するクラス
class CookieHandlerJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Cookieヘッダーからaccess_tokenを取得
        access_token = request.COOKIES.get("access_token")
        logger.debug(access_token)


        if not access_token:
            logger.error("no token")
            Response({"message": "no Token"})

        else:
            Response(access_token)

        if access_token:
            request.META["HTTP_AUTHORIZATION"] = "{header_type} {access_token}".format(
                header_type=settings.SIMPLE_JWT["AUTH_HEADER_TYPES"][0],
                access_token=access_token,
            )

        return super().authenticate(request)