from django.core.management.base import BaseCommand
from in_brief.domain.models import Article, Category
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate In Brief with comprehensive institutional content'

    def handle(self, *args, **options):
        User = get_user_model()
        author, created = User.objects.get_or_create(
            username='alessandra',
            defaults={
                'email': 'amdonadonadvocacia@adv.oabsp.org.br',
                'first_name': 'Alessandra',
                'last_name': 'Donadon',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            author.set_password('admin123')
            author.save()
            self.stdout.write(self.style.SUCCESS(f'Created author: {author.username}'))

        # Create Categories
        categories_data = [
            {"name": "Saúde", "slug": "saude"},
            {"name": "Cultural", "slug": "cultural"},
            {"name": "Consumidor", "slug": "consumidor"},
            {"name": "Terceiro Setor", "slug": "terceiro-setor"},
        ]
        
        cat_map = {}
        for data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=data['slug'],
                defaults={'name': data['name']}
            )
            cat_map[data['slug']] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat.name}'))

        articles_data = [
            {
                "title": "Lipedema: Direitos do Paciente Frente aos Planos de Saúde",
                "slug": "lipedema-direitos-paciente",
                "category": cat_map.get("saude"),
                "summary": "O lipedema é uma condição crônica que afeta milhões de mulheres. Entenda seus direitos na luta contra negativas de cobertura.",
                "content": "<h2>O que é Lipedema?</h2><p>O lipedema é uma doença crônica, progressiva e hereditária que afeta principalmente mulheres...</p>"
            },
            {
                "title": "Lei Rouanet: Como Regularizar Projetos Culturais",
                "slug": "lei-rouanet-regularizacao",
                "category": cat_map.get("cultural"),
                "summary": "Entenda o processo de regularização documental para acesso a incentivos culturais via Lei Rouanet.",
                "content": "<h2>A Importância da Regularização</h2><p>A Lei Rouanet (Lei nº 8.313/91) é um dos principais mecanismos de fomento à cultura no Brasil...</p>"
            },
            {
                "title": "Superendividamento: A Lei que Protege o Consumidor",
                "slug": "superendividamento-lei-protecao",
                "category": cat_map.get("consumidor"),
                "summary": "A Lei do Superendividamento oferece ferramentas para reorganização financeira e preservação da dignidade.",
                "content": "<h2>O que é Superendividamento?</h2><p>É a impossibilidade manifesta de o consumidor pagar a totalidade de suas dívidas...</p>"
            },
            {
                "title": "Terceiro Setor: Assessoria para ONGs e Fundações",
                "slug": "terceiro-setor-assessoria-ongs",
                "category": cat_map.get("terceiro-setor"),
                "summary": "Organizações do terceiro setor precisam de suporte jurídico para cumprir sua missão social com segurança.",
                "content": "<h2>O Papel do Terceiro Setor</h2><p>ONGs desempenham papel fundamental na promoção de direitos humanos...</p>"
            }
        ]

        for data in articles_data:
            article, created = Article.objects.get_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'content': data['content'],
                    'summary': data['summary'],
                    'author': author,
                    'is_published': True,
                    'published_at': timezone.now()
                }
            )
            
            if created:
                if data.get('category'):
                    article.categories.add(data['category'])
                self.stdout.write(self.style.SUCCESS(f'Created article: {article.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Article already exists: {article.title}'))
