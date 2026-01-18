import re
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class PIIRedactionMiddleware:
    """
    Middleware to redact PII (CPF, Email, Phone) from logs and potentially responses types if configured.
    Currently focuses on logging.
    """
    PII_PATTERNS = {
        'cpf': r'\d{3}\.\d{3}\.\d{3}-\d{2}',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\(\d{2}\)\s\d{4,5}-\d{4}',
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Request inspection logic here (if needed) or simple pass-through with logging
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Ensure we don't log raw PII in exceptions if we can help it
        # This is a placeholder for more advanced scrubbing logic
        pass

    @staticmethod
    def redact(text):
        if not isinstance(text, str):
            return text
        for name, pattern in PIIRedactionMiddleware.PII_PATTERNS.items():
            text = re.sub(pattern, f'[REDACTED {name.upper()}]', text)
        return text
