from django.utils.text import slugify
from django.utils import timezone
from django.db import transaction
from in_brief.domain.models import Article, Category
from typing import List

class ArticleService:
    @staticmethod
    @transaction.atomic
    def create_article(title: str, content: str, author, category_ids: List[int], is_published: bool = False) -> Article:
        slug = slugify(title)
        # Handle duplicate slugs logic here if needed, for simplicty assuming unique title/slug
        
        article = Article(
            title=title,
            slug=slug,
            content=content,
            author=author,
            is_published=is_published,
            published_at=timezone.now() if is_published else None,
            summary=content[:150] + "..." if len(content) > 150 else content
        )
        article.save()
        
        if category_ids:
            categories = Category.objects.filter(id__in=category_ids)
            article.categories.set(categories)
            
        return article

    @staticmethod
    def get_published_articles():
        return Article.objects.filter(is_published=True).prefetch_related('categories')
