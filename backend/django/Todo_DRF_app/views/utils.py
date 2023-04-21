import jwt
from jwt.exceptions import DecodeError
from rest_framework import status
from rest_framework.exceptions import NotFound,APIException
from Todo_DRF.settings import settings_dev as settings

def get_payload(JWT):
        try:
            return jwt.decode(jwt=str(JWT), key=settings.SECRET_KEY, algorithms=["HS256"],)
        except DecodeError as e:
            # APIExceptionはraiseすると自動的にHTTPレスポンスを作ってユーザーに返される
            print(type(JWT),JWT)
            raise APIException(detail="デコードに失敗しました")