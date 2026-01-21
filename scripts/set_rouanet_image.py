
import os
import django
from django.core.files import File
import sys

# Setup Django
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from in_brief.models import Article

def run():
    # Source image path (project root)
    image_path = os.path.join(os.path.dirname(__file__), '../lei rouanet.png')
    
    if not os.path.exists(image_path):
        print(f"Error: File not found at {image_path}")
        return

    # Find Article
    # Searching for title loop or similar
    article = Article.objects.filter(title__icontains="Lei Rouanet").first()
    
    if not article:
        print("Error: Article 'Lei Rouanet' not found.")
        return

    print(f"Found article: {article.title}")
    
    # Check if already has image to avoid overwriting unnecessarily or dupes? 
    # User asked to put it, so we overwrite.
    
    with open(image_path, 'rb') as f:
        article.image.save('lei_rouanet.png', File(f), save=True)
        print(f"Successfully saved image to article '{article.title}'")

if __name__ == "__main__":
    run()
