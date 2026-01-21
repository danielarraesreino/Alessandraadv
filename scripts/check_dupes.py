
import os
import django
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from in_brief.models import Article

def check_dupes():
    for term in ["Lipedema", "Golpes Bancários"]:
        articles = Article.objects.filter(title__icontains=term)
        print(f"Articles matching '{term}': {articles.count()}")
        for a in articles:
            print(f"- {a.title} (Slug: {a.slug})")

if __name__ == "__main__":
    check_dupes()
