"""
Test Error Notification System

Simple test view to validate error capture, WhatsApp notification, and email alerts.
"""
from django.http import HttpResponse
from django.views import View


class TestErrorView(View):
    """
    Test view that raises an intentional exception.
    Access: /test-error/
    """
    
    def get(self, request):
        """Intentionally raise an exception to test error notification system."""
        raise Exception("TEST ERROR: This is a simulated exception to validate Mission 1 error notification system")


def test_error_function_view(request):
    """Function-based test view."""
    raise ValueError("TEST ERROR: Function-based view exception")
