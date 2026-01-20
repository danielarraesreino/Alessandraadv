from django.shortcuts import render
from .domain.models import Article

def index(request):
    """List of published articles."""
    articles = Article.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'in_brief/article_list.html', {'articles': articles})

def article_detail(request, slug):
    """
    Display a specific article based on slug.
    Since we don't have the text file yet, we use placeholders
    reusing the teaser content.
    """
    articles = {
        'lei-rouanet': {
            'title': 'Lei Rouanet e Regularização',
            'content': 'Por que a regularização documental é o primeiro passo para o fomento cultural? Entenda como estruturar Estatutos, Atas e CNPJ para acessar leis de incentivo. (Conteúdo completo pendente de envio)'
        },
        'lipedema': {
            'title': 'Lipedema e Planos de Saúde',
            'content': 'A abusividade das negativas e o caminho para garantir o tratamento. Conheça seus direitos e como enfrentar recusas de cirurgias, exames e tratamentos. (Conteúdo completo pendente de envio)'
        },
        'superendividamento': {
            'title': 'Superendividamento (Lei 14.181/21)',
            'content': 'Como a Lei 14.181/21 protege o mínimo existencial e reorganiza sua vida financeira. Descubra os mecanismos de renegociação e proteção do consumidor. (Conteúdo completo pendente de envio)'
        }
    }
    
    article = articles.get(slug)
    if not article:
        # Fallback for unknown slugs or future articles
        article = {
            'title': slug.replace('-', ' ').title(),
            'content': None # Will trigger the 'Em breve' message in template
        }
    
    return render(request, 'in_brief/article_detail.html', article)
