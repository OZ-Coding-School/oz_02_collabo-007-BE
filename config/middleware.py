from .loggers import Logger


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = Logger()

    def __call__(self, request):
        response = self.get_response(request)
        return response
