
import os
import django
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from in_brief.models import Article

def check_content():
    # Target the NEW article
    slug = 'lei-rouanet-o-que-voce-precisa-saber-e-talvez-ainda-nao-saiba'
    article = Article.objects.filter(slug=slug).first()
    
    if not article:
        print("Article not found!")
        return

    print(f"Checking article: {article.title}")
    if article.content and "Muito se fala" in article.content:
        print("SUCCESS: Content found.")
        print(f"Content length: {len(article.content)}")
    else:
        print("FAILURE: Content missing or incorrect.")

if __name__ == "__main__":
    check_content()
