from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from in_brief.domain.models import Article, Category
from in_brief.services.article_service import ArticleService

class Command(BaseCommand):
    help = 'Populates the database with initial In Brief articles'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        # Create a default admin user if none exists (for author attribution)
        if not User.objects.filter(username='admin').exists():
            author = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Created superuser "admin"'))
        else:
            author = User.objects.get(username='admin')

        # Categories
        categories_data = ['Cultural', 'Saúde', 'Financeiro']
        categories = {}
        for name in categories_data:
            cat, created = Category.objects.get_or_create(name=name, slug=name.lower())
            categories[name] = cat
            if created:
                self.stdout.write(f'Created category: {name}')

        # Articles
        articles_data = [
            {
                'title': 'Entendendo a Lei Rouanet',
                'content': 'A Lei Rouanet é o principal mecanismo de fomento à cultura no Brasil. Ela permite que empresas e cidadãos destinem parte do seu Imposto de Renda para projetos culturais aprovados...',
                'category': 'Cultural',
                'slug': 'entendendo-a-lei-rouanet'
            },
            {
                'title': 'Lipedema: Direitos e Tratamentos',
                'content': 'O lipedema é uma doença crônica reconhecida recentemente pela CID-11. Muitas pacientes enfrentam dificuldades para conseguir cobertura de tratamento pelos planos de saúde...',
                'category': 'Saúde',
                'slug': 'lipedema-direitos-e-tratamentos'
            },
            {
                'title': 'Superendividamento e a Defesa do Consumidor',
                'content': 'A Lei do Superendividamento trouxe novos mecanismos para repactuação de dívidas, visando preservar o mínimo existencial do consumidor e evitar a exclusão social...',
                'category': 'Financeiro',
                'slug': 'superendividamento-e-defesa-do-consumidor'
            }
        ]

        for data in articles_data:
            if not Article.objects.filter(slug=data['slug']).exists():
                cat = categories[data['category']]
                # Using Service to create (simulating app usage, though direct create is fine for seeds)
                article = ArticleService.create_article(
                    title=data['title'],
                    content=data['content'],
                    author=author,
                    category_ids=[cat.id],
                    is_published=True
                )
                self.stdout.write(self.style.SUCCESS(f'Created article: {data["title"]}'))
            else:
                self.stdout.write(f'Article already exists: {data["title"]}')
