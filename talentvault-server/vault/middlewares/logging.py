import logging

logger = logging.getLogger('vault.api')

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            logger.info(f"Request: {request.method} {request.path}")
            response = self.get_response(request)
            logger.info(f"Response: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Error: {e} - {request.method} {request.path}")
            raise e