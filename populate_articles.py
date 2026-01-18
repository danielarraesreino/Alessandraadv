import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from in_brief.domain.models import Article, Category
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(is_superuser=True).first()

if not admin_user:
    print("No admin user found.")
    exit()

articles_data = [
    {
        "title": "Lei Rouanet",
        "slug": "lei-rouanet",
        "content": "A regularização documental é a chave para o fomento cultural. Estruturamos estatutos e atas para garantir acesso a incentivos.",
        "summary": "Impacto da regularização documental.",
        "category": "Cultural"
    },
    {
        "title": "Lipedema",
        "slug": "lipedema",
        "content": "Defendemos os direitos do paciente frente às negativas abusivas dos convênios para cirurgias e tratamentos de lipedema.",
        "summary": "Direitos do paciente e negativas.",
        "category": "Saúde"
    },
    {
        "title": "Superendividamento",
        "slug": "superendividamento",
        "content": "A Lei 14.181/21 traz novos mecanismos para proteção do mínimo existencial e repactuação de dívidas.",
        "summary": "Ferramenta de dignidade financeira.",
        "category": "Consumidor"
    }
]

for data in articles_data:
    cat, _ = Category.objects.get_or_create(name=data['category'], defaults={'slug': data['category'].lower()})
    article, created = Article.objects.get_or_create(
        slug=data['slug'],
        defaults={
            "title": data['title'],
            "content": data['content'],
            "summary": data['summary'],
            "author": admin_user,
            "is_published": True,
            "published_at": timezone.now()
        }
    )
    article.categories.add(cat)
    article.save()
    print(f"Article '{article.title}' ensured.")
