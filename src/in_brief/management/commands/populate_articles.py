from django.core.management.base import BaseCommand
from in_brief.domain.models import Article, Category
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate In Brief with initial articles'

    def handle(self, *args, **options):
        User = get_user_model()
        author = User.objects.first()
        if not author:
            author = User.objects.create_superuser('admin_content', 'admin@example.com', 'password')

        # Create Categories
        cat_insights, _ = Category.objects.get_or_create(name='Insights Jurídicos', slug='insights')
        cat_news, _ = Category.objects.get_or_create(name='Notícias do Escritório', slug='noticias')

        articles_data = [
            {
                'title': 'Lei Rouanet e Regularização Documental',
                'summary': 'Entenda a importância da regularização documental para acesso a leis de incentivo.',
                'content': '<p>A regularização documental é o primeiro passo para o fomento cultural. Sem Estatutos, Atas e CNPJ em dia, o acesso a leis como a Rouanet torna-se impossível. Neste artigo, exploramos o passo a passo para garantir que sua entidade esteja apta a captar recursos.</p><h3>Principais Documentos</h3><ul><li>Estatuto Social atualizado</li><li>Ata de Eleição e Posse vigente</li><li>CNPJ ativo e regular</li></ul>',
                'category': cat_insights
            },
            {
                'title': 'Direitos no Tratamento do Lipedema',
                'summary': 'Saiba como enfrentar negativas de planos de saúde para cirurgias e tratamentos.',
                'content': '<p>O Lipedema é uma doença crônica reconhecida pela OMS, mas muitos planos de saúde ainda negam cobertura para seu tratamento cirúrgico. A jurisprudência tem avançado no sentido de garantir o direito das pacientes, considerando a cirurgia não como estética, mas como reparadora e funcional.</p>',
                'category': cat_insights
            },
            {
                'title': 'Superendividamento: Um Novo Começo',
                'summary': 'A Lei 14.181/21 e a proteção do mínimo existencial para consumidores.',
                'content': '<p>A Lei do Superendividamento trouxe mecanismos importantes para a repactuação de dívidas, garantindo que o consumidor possa reorganizar sua vida financeira sem comprometer sua subsistência. Entenda como funciona o processo de conciliação e revisão contratual.</p>',
                'category': cat_news
            }
        ]

        for data in articles_data:
            slug = slugify(data['title'])
            if not Article.objects.filter(slug=slug).exists():
                article = Article.objects.create(
                    title=data['title'],
                    slug=slug,
                    summary=data['summary'],
                    content=data['content'],
                    author=author,
                    is_published=True,
                    published_at=timezone.now()
                )
                article.categories.add(data['category'])
                self.stdout.write(self.style.SUCCESS(f'Created article: {article.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Article already exists: {data["title"]}'))
