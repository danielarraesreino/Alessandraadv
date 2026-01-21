
import os
import django
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from in_brief.models import Article

def list_slugs():
    articles = Article.objects.all()
    print(f"Total articles: {articles.count()}")
    for a in articles:
        print(f"Title: {a.title}")
        print(f"Slug: {a.slug}")
        print(f"Published: {a.is_published}")
        print(f"Date: {a.published_at}")
        print("-" * 20)

if __name__ == "__main__":
    list_slugs()
