from logging import config,getLogger
from Todo_DRF.settings import settings_dev as settings
import json

config.dictConfig(settings.LOGGING)
logger = getLogger('django_file_logger')

class RequestLoggingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        
        print(request.body.decode('utf-8'))
        
        
        # リクエストがビューに到達する前に実行される
        # self.process_request(request)

        # ビューの処理
        response = self.get_response(request)

        print(response)

        # リクエストがビューに到達した後に実行される
        # self.process_response(request,response)

        return response

    def process_request(self,request):
        logger.debug(f"request.data:{request.data}")
        
    # def process_response(self,request,response):
        
