from .loggers import Logger

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = Logger()

    def __call__(self, request):
        self.logger.debug(f"Request to {request.path}")
        response = self.get_response(request)
        self.logger.debug(f"Response status: {response.status_code}")
        return response
