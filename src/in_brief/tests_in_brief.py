import pytest
from in_brief.domain.models import Article, Category
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_create_article():
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="password")
    category = Category.objects.create(name="Tech", slug="tech")
    
    article = Article.objects.create(
        title="Test Article",
        slug="test-article",
        content="Values",
        author=user
    )
    article.categories.add(category)
    
    assert article.pk is not None
    assert article.categories.count() == 1
    assert str(article) == "Test Article"
