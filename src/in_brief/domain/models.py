from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    slug = models.SlugField(unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    content = RichTextUploadingField(verbose_name="Conteúdo")
    summary = models.TextField(blank=True, verbose_name="Resumo")
    image = models.ImageField(upload_to='articles/', null=True, blank=True, verbose_name="Imagem de Capa")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Autor")
    categories = models.ManyToManyField(Category, related_name="articles", verbose_name="Categorias")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    is_published = models.BooleanField(default=False, verbose_name="Está publicado?")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Data de Publicação")

    class Meta:
        verbose_name = "Artigo"
        verbose_name_plural = "Artigos"

    def __str__(self):
        return self.title
