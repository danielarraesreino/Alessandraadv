from ninja import Schema
from datetime import datetime
from typing import List, Optional

class CategoryOut(Schema):
    id: int
    name: str
    slug: str

class ArticleIn(Schema):
    title: str
    content: str
    category_ids: List[int] = []
    is_published: bool = False

class ArticleOut(Schema):
    id: int
    title: str
    slug: str
    summary: str
    content: str
    author_id: int
    categories: List[CategoryOut]
    created_at: datetime
    published_at: Optional[datetime]
    is_published: bool
