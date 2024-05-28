import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('django')

class LogRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 요청 헤더 로깅
        headers = dict(request.headers)
        # 'Cookie'와 같이 민감한 정보를 포함할 수 있는 헤더는 제외
        headers.pop('Cookie', None)

        # 요청 메타데이터 로깅
        # logger.info(f"Request path: {request.path}")
        # logger.info(f"Request method: {request.method}")
        # logger.info(f"Request headers: {headers}")

    def process_response(self, request, response):
        # 응답 메타데이터 로깅
        # logger.info(f"Response status code: {response.status_code}")
        # 응답 내용은 로깅에서 제외
        return response
