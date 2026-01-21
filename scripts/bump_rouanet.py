
import os
import django
import sys
from django.utils import timezone

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from in_brief.models import Article

def run():
    article = Article.objects.filter(title__icontains="Lei Rouanet").first()
    if article:
        article.published_at = timezone.now()
        article.save()
        print(f"Bumped '{article.title}' to {article.published_at}")
    else:
        print("Article not found")

if __name__ == "__main__":
    run()
