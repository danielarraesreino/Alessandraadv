
import os
import django
from django.core.files import File
from django.utils import timezone
import sys

# Setup Django
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from in_brief.models import Article

def run():
    # Source image path (project root)
    image_filename = "RECUPERAR VALORES DE GOLPES BANCÁRIOS: UM DIREITO DO CONSUMIDOR.png"
    image_path = os.path.join(os.path.dirname(__file__), f'../{image_filename}')
    
    if not os.path.exists(image_path):
        print(f"Error: File not found at {image_path}")
        return

    # Find Article
    article = Article.objects.filter(title__icontains="GOLPES BANCÁRIOS").first()
    
    if not article:
        print("Error: Article 'Golpes Bancários' not found.")
        return

    print(f"Found article: {article.title}")
    
    with open(image_path, 'rb') as f:
        article.image.save('golpes_bancarios.png', File(f), save=True)
        print(f"Successfully saved image to article '{article.title}'")

    # Bump date to appear on top
    article.published_at = timezone.now()
    article.save()
    print(f"Bumped '{article.title}' to {article.published_at}")

if __name__ == "__main__":
    run()
