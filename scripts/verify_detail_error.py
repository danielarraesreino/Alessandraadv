
import os
import django
import sys
from django.test import Client

# Setup Django
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from in_brief.models import Article

def verify_detail():
    client = Client()
    # Find the Lei Rouanet article slug
    article = Article.objects.filter(title__icontains="Lei Rouanet").first()
    # Or explicitly:
    # article = Article.objects.get(slug='lei-rouanet-o-que-voce-precisa-saber-e-talvez-ainda-nao-saiba')
    if not article:
        print("Article not found!")
        return

    url = f'/in-brief/{article.slug}'
    print(f"Requesting {url} ...")
    
    try:
        response = client.get(url, SERVER_NAME='127.0.0.1')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            if "Lei Rouanet" in content:
                print("SUCCESS: Detail page content found.")
            if "img src" in content:
                print("SUCCESS: Image tag found.")
            else:
                print("WARNING: Image tag NOT found (maybe logic error?)")
                
            # The script currently doesn't check specific slugs for everything, just content. 
            # But verifies content for current page context.
            # Lei Rouanet check is fine (uses new slug).
            
            # We can add a quick check for other articles by querying DB directly here to be sure they exist and have images.
            lipedema = Article.objects.filter(title__icontains="Lipedema").first()
            if lipedema and lipedema.image:
                print(f"SUCCESS: Lipedema article '{lipedema.title}' has image: {lipedema.image.name}")
            else:
                print("FAILURE: Lipedema article missing or no image.")

            golpes = Article.objects.filter(title__icontains="Golpes").first()
            if golpes and golpes.image:
                print(f"SUCCESS: Golpes article '{golpes.title}' has image: {golpes.image.name}")
            else:
                print("FAILURE: Golpes article missing or no image.")
            # Check content
            if "Muito se fala" in content:
                 print("SUCCESS: Article content found.")
            else:
                 print("FAILURE: Article content seems missing.")
        else:
            print("FAILURE: Non-200 status code.")
            
    except Exception as e:
        print(f"EXCEPTION OCCURRED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_detail()
