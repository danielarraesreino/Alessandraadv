
import os
import django
from django.core.files import File
import sys

# Setup Django
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from in_brief.models import Article

def fix_data():
    correct_slug = 'lei-rouanet-o-que-voce-precisa-saber-e-talvez-ainda-nao-saiba'
    correct_article = Article.objects.filter(slug=correct_slug).first()
    
    if not correct_article:
        print("Correct article not found!")
        return

    # Assign Image
    image_path = os.path.join(os.path.dirname(__file__), '../lei rouanet.png')
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            correct_article.image.save('lei_rouanet.png', File(f), save=True)
            print(f"Assigned image to '{correct_article.title}'")
    else:
        print("Image file not found!")

    # Cleanup Duplicates
    duplicates = Article.objects.filter(title__icontains="Lei Rouanet").exclude(slug=correct_slug)
    count = duplicates.count()
    if count > 0:
        print(f"Deleting {count} duplicate/legacy articles...")
        duplicates.delete()
        print("Duplicates deleted.")
    else:
        print("No duplicates found.")

if __name__ == "__main__":
    fix_data()
