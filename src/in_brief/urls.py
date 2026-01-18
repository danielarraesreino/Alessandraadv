from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='in_brief_index'),
    path('<slug:slug>', views.article_detail, name='article_detail'),
]
