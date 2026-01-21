
import os
import django
from django.test import RequestFactory
import sys

# Setup Django
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from core.views import home
# from in_brief.views import article_list 
# Note: article_list might be a class-based view or function. 
# Checking in_brief/urls.py would confirm, but usually it's passed as a view.
# I'll check urls first if this fails, but let's assume standard pattern.
# Actually, let's just use the Client.

from django.test import Client
from in_brief.models import Article

def verify():
    client = Client()
    
    # Verify Home
    print("Verifying Home Page...")
    response = client.get('/', SERVER_NAME='127.0.0.1')
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        if "Lei Rouanet" in content:
            print("SUCCESS: Home page contains 'Lei Rouanet'")
        else:
            print("FAILURE: Home page missing 'Lei Rouanet'")
            
        if "lei_rouanet.png" in content:
            print("WARNING: Home page contains 'lei_rouanet.png' image (Unexpected but ok)")
        
        if "In Brief" in content:
            print("SUCCESS: Home page contains 'In Brief' section")
    else:
        print(f"FAILURE: Home page returned {response.status_code}")

    # Verify In Brief List
    print("\nVerifying In Brief List Page...")
    response = client.get('/in-brief/', SERVER_NAME='127.0.0.1') # Assuming this is the url
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        if "Lei Rouanet" in content:
             print("SUCCESS: In Brief page contains 'Lei Rouanet'")
        
        if "lei_rouanet.png" in content:
            print("SUCCESS: In Brief page contains 'lei_rouanet.png' image")
        else:
            print("FAILURE: In Brief page MISSING 'lei_rouanet.png' image")

        if "golpes_bancarios.png" in content:
            print("SUCCESS: In Brief page contains 'golpes_bancarios.png' image")
        else:
            print("FAILURE: In Brief page MISSING 'golpes_bancarios.png' image")

        if "lipedema.png" in content:
            print("SUCCESS: In Brief page contains 'lipedema.png' image")
        else:
            print("FAILURE: In Brief page MISSING 'lipedema.png' image")
        
        # Check for social links
        
        # Check for social links
        if "wa.me" in content:
            print("SUCCESS: WhatsApp link found")
        else:
            print("FAILURE: WhatsApp link NOT found")
            
        if "linkedin.com" in content:
            print("SUCCESS: LinkedIn link found")
    else:
         print(f"FAILURE: In Brief page returned {response.status_code}")

if __name__ == "__main__":
    verify()
