import logging
import traceback
import sys

logger = logging.getLogger(__name__)

class DiagnosticMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f">>> REQUEST START: {request.method} {request.path} <<<")
        try:
            response = self.get_response(request)
            print(f">>> REQUEST SUCCESS: {request.method} {request.path} -> {response.status_code} <<<")
            return response
        except Exception as e:
            print(f">>> REQUEST EXCEPTION: {e} <<<")
            traceback.print_exc(file=sys.stdout)
            raise
