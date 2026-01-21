
import os
import django
import sys
from django.utils import timezone

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from in_brief.models import Article

def run():
    articles = Article.objects.filter(is_published=True, published_at__isnull=True)
    count = articles.count()
    print(f"Found {count} published articles with no published_at date.")
    
    for article in articles:
        article.published_at = article.created_at or timezone.now()
        article.save()
        print(f"Updated {article.title} with published_at={article.published_at}")

if __name__ == "__main__":
    run()
