import uuid
import logging
from django.conf import settings
from django.shortcuts import render

logger = logging.getLogger(__name__)

class TechnicalSupportMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

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
        Capture diagnostic info when an error occurs.
        """
        error_id = str(uuid.uuid4())[:8].upper()
        
        # Log basic info (avoiding LGPD sensitive data)
        logger.error(f"SYSTEM_ERROR [{error_id}]: {str(exception)} | Path: {request.path} | User: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
        
        # Attach error_id to request for the template
        request.error_id = error_id
        
        # In production (DEBUG=False), we return a custom response or let Django handle it via handler500
        # If we return None here, Django's default exception handling takes over.
        return None
