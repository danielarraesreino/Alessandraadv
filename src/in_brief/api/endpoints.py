from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from in_brief.services.article_service import ArticleService
from in_brief.api.schemas import ArticleIn, ArticleOut
from in_brief.domain.models import Article

router = Router()

@router.post("/articles", response=ArticleOut)
def create_article(request, payload: ArticleIn):
    # In a real app, 'request.user' would be used. 
    # For this skeleton, we assume an authenticated user or mock it.
    # We'll use request.user if available, else standard django behavior requires auth.
    
    article = ArticleService.create_article(
        title=payload.title,
        content=payload.content,
        author=request.user,
        category_ids=payload.category_ids,
        is_published=payload.is_published
    )
    return article

@router.get("/articles", response=List[ArticleOut])
def list_articles(request):
    return ArticleService.get_published_articles()
