from django.shortcuts import render, get_object_or_404
from .domain.models import Article

def index(request):
    """List of published articles."""
    articles = Article.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'in_brief/article_list.html', {'articles': articles})

def article_detail(request, slug):
    """Display a specific article based on slug from database."""
    article = get_object_or_404(Article, slug=slug, is_published=True)
    return render(request, 'in_brief/article_detail.html', {'article': article, 'debug_var': 'DEBUG_SUCCESS'})
