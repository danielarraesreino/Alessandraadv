
import os
import django
from django.core.files import File
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from in_brief.models import Article

def consolidate():
    # --- LIPEDEMA ---
    target_slug = 'lipedema-o-plano-de-saude-nao-pode-ignorar'
    target_article = Article.objects.filter(slug=target_slug).first()
    
    if target_article:
        # Re-assign image just to be sure (if source exists)
        img_path = os.path.join(os.path.dirname(__file__), '../lipodemia.png')
        if os.path.exists(img_path):
             with open(img_path, 'rb') as f:
                target_article.image.save('lipedema.png', File(f), save=True)
                print(f"Assigned image to NEW Lipedema article: {target_article.title}")
        
        # Delete duplicates (everything with Lipedema in title EXCEPT target)
        dupes = Article.objects.filter(title__icontains="Lipedema").exclude(slug=target_slug)
        print(f"Deleting {dupes.count()} Lipedema duplicates...")
        dupes.delete()
    else:
        print("Target Lipedema article not found!")

    # --- GOLPES ---
    # The target is the one I assigned image to in Step 164, which was found by title title__icontains="GOLPES BANCÁRIOS"
    # Step 215 showed the one with image is: RECUPERAR VALORES DE GOLPES BANCÁRIOS: UM DIREITO DO CONSUMIDOR!
    # Slug: recuperar-valores-de-golpes-bancarios-um-direito-do-consumidor
    
    golpes_slug = 'recuperar-valores-de-golpes-bancarios-um-direito-do-consumidor'
    golpes_target = Article.objects.filter(slug=golpes_slug).first()
    
    if golpes_target:
        # Delete duplicates (Legacy one: golpes-bancarios-direitos)
        dupes = Article.objects.filter(title__icontains="Golpes Bancários").exclude(slug=golpes_slug)
        # Note: Title query is case insensitive generally if using sqlite, but let's be broad
        # Step 215 showed `Recuperar Valores de Golpes Bancários...` so it should match
        print(f"Deleting {dupes.count()} Golpes duplicates...")
        dupes.delete()
    else:
        print("Target Golpes article not found!")

if __name__ == "__main__":
    consolidate()
