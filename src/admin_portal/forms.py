from django import forms
from in_brief.models import Article, Category

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'summary', 'content', 'categories', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'style': 'width: 100%; padding: 0.75rem; border: 1px solid var(--color-gray-light); border-radius: 8px;',
                'placeholder': 'Título do artigo'
            }),
            'summary': forms.Textarea(attrs={
                'style': 'width: 100%; padding: 0.75rem; border: 1px solid var(--color-gray-light); border-radius: 8px;',
                'rows': 3,
                'placeholder': 'Breve resumo para as redes sociais/home'
            }),
            'categories': forms.SelectMultiple(attrs={
                'style': 'width: 100%; padding: 0.75rem; border: 1px solid var(--color-gray-light); border-radius: 8px;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom styles for the checkbox if needed, but usually default is fine
        self.fields['is_published'].widget.attrs.update({'style': 'width: 20px; height: 20px;'})
