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
        "title": "Lei Rouanet e o Terceiro Setor",
        "slug": "lei-rouanet",
        "content": "A regularização documental é a chave para o fomento cultural. Estruturamos estatutos e atas para garantir acesso a incentivos e parcerias com o setor público.",
        "summary": "Impacto da regularização documental na captação de recursos.",
        "category": "Cultural"
    },
    {
        "title": "Lipedema: Direitos à Saúde e Cobertura de Cirurgias",
        "slug": "lipedema",
        "content": "Defendemos os direitos do paciente frente às negativas abusivas dos convênios para cirurgias e tratamentos de lipedema, garantindo o acesso ao tratamento digno.",
        "summary": "Proteção jurídica contra negativas de planos de saúde.",
        "category": "Saúde"
    },
    {
        "title": "Lei do Superendividamento: O Mínimo Existencial",
        "slug": "superendividamento",
        "content": "A Lei 14.181/21 traz novos mecanismos para proteção do mínimo existencial e repactuação de dívidas, oferecendo uma segunda chance para a dignidade financeira.",
        "summary": "Mecanismos de defesa para o consumidor endividado.",
        "category": "Consumidor"
    },
    {
        "title": "Terceiro Setor: Governança e Transparência",
        "slug": "terceiro-setor",
        "content": "A assessoria jurídica para ONGs e fundações garante a conformidade com as exigências legais de transparência, essencial para a manutenção de parcerias e doações.",
        "summary": "Gestão jurídica estratégica para organizações sociais.",
        "category": "Terceiro Setor"
    },
    {
        "title": "LGPD na Advocacia: Proteção de Dados Sensíveis",
        "slug": "lgpd-advocacia",
        "content": "O tratamento de dados pessoais no ambiente jurídico exige rigor técnico. Implementamos protocolos de segurança para garantir a conformidade integral com a LGPD.",
        "summary": "Segurança e privacidade no tratamento de informações jurídicas.",
        "category": "Tecnologia"
    },
    {
        "title": "Direito Civil e a Prevenção de Conflitos",
        "slug": "direito-civil-prevencao",
        "content": "A advocacia consultiva e preventiva no Direito Civil evita longas disputas judiciais através de contratos bem estruturados e mediação estratégica.",
        "summary": "Estratégias de prevenção de litígios e segurança jurídica.",
        "category": "Civil"
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
