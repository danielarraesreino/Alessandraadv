"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add src to sys.path to allow imports from root of src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(">>> LOADING WSGI APPLICATION <<<")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
print(f">>> SETTINGS MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')} <<<")

try:
    application = get_wsgi_application()
    print(">>> WSGI APPLICATION LOADED SUCCESSFULLY <<<")
except Exception as e:
    print(f">>> ERROR LOADING WSGI APPLICATION: {e} <<<")
    raise
