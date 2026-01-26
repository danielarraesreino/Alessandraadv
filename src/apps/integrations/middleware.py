import logging
from django.conf import settings
from apps.integrations.error_handler import ErrorHandler

logger = logging.getLogger(__name__)

class TechnicalSupportMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.error_handler = ErrorHandler()

    def __call__(self, request):
        # Add basic dev status to request
        request.is_daniel = False
        if request.user.is_authenticated:
            if request.user.username == 'daniel' or request.user.groups.filter(name='Technical_Support').exists():
                request.is_daniel = True
        
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """
        Capture diagnostic info and notify relevant parties on error.
        
        Mission 1: Proactive Notification System
        """
        # Use centralized error handler service
        error_id = self.error_handler.capture_error(
            exception=exception,
            request=request
        )
        
        # Attach error_id to request for modal rendering
        request.error_id = error_id
        
        # Return None to allow Django's standard error handling
        # The error_modal.html will render if error_id is present
        return None
