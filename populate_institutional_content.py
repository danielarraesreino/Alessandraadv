#!/usr/bin/env python
"""
Populate Institutional Content - Plataforma Dra. Alessandra Donadon
===================================================================
Este script popula o banco de dados com:
- Categorias (Saúde, Cultural, Consumidor, Terceiro Setor)
- Artigos "In Brief" com conteúdo institucional
"""

import os
import sys
import django
from django.utils import timezone
from django.utils.text import slugify

# Configure Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model
from in_brief.domain.models import Category, Article

User = get_user_model()


def get_or_create_author():
    """Get or create default author (Alessandra)"""
    author, created = User.objects.get_or_create(
        username='alessandra',
        defaults={
            'email': 'amdonadonadvocacia@adv.oabsp.org.br',
            'first_name': 'Alessandra',
            'last_name': 'Donadon',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        author.set_password('admin123')  # Change in production!
        author.save()
        print(f"✅ Created author: {author}")
    return author


def create_categories():
    """Create article categories"""
    categories_data = [
        {"name": "Saúde", "slug": "saude"},
        {"name": "Cultural", "slug": "cultural"},
        {"name": "Consumidor", "slug": "consumidor"},
        {"name": "Terceiro Setor", "slug": "terceiro-setor"},
        {"name": "Direito Civil", "slug": "direito-civil"},
    ]
    
    categories = []
    for data in categories_data:
        cat, created = Category.objects.get_or_create(
            slug=data['slug'],
            defaults={'name': data['name']}
        )
        categories.append(cat)
        if created:
            print(f"✅ Created category: {cat.name}")
    
    return categories


def create_articles(author, categories):
    """Create institutional articles"""
    
    # Map categories for easy access
    cat_map = {cat.slug: cat for cat in categories}
    
    articles_data = [
        {
            "title": "Lipedema: Direitos do Paciente Frente aos Planos de Saúde",
            "slug": "lipedema-direitos-paciente",
            "category": cat_map.get("saude"),
            "summary": "O lipedema é uma condição crônica que afeta milhões de mulheres. Entenda seus direitos na luta contra negativas de cobertura.",
            "content": """
                <h2>O que é Lipedema?</h2>
                <p>O lipedema é uma doença crônica, progressiva e hereditária que afeta principalmente mulheres, 
                caracterizada pelo acúmulo desproporcional de gordura em membros inferiores e, em alguns casos, 
                superiores.</p>
                
                <h2>Negativas de Cobertura</h2>
                <p>Muitos planos de saúde negam a cobertura de tratamentos alegando caráter estético. 
                No entanto, a jurisprudência brasileira tem se posicionado favoravelmente aos pacientes, 
                reconhecendo o lipedema como doença funcional.</p>
                
                <h2>Seus Direitos</h2>
                <ul>
                    <li>Direito à cobertura de cirurgia de lipoaspiração quando indicada por médico</li>
                    <li>Direito ao tratamento multidisciplinar (fisioterapia, drenagem linfática)</li>
                    <li>Direito à segunda opinião médica</li>
                </ul>
                
                <p><strong>Se você ou alguém que você conhece sofre com lipedema e teve negativa de cobertura, 
                procure seus direitos. A advocacia especializada pode fazer a diferença.</strong></p>
            """
        },
        {
            "title": "Lei Rouanet: Como Regularizar Projetos Culturais",
            "slug": "lei-rouanet-regularizacao",
            "category": cat_map.get("cultural"),
            "summary": "Entenda o processo de regularização documental para acesso a incentivos culturais via Lei Rouanet.",
            "content": """
                <h2>A Importância da Regularização</h2>
                <p>A Lei Rouanet (Lei nº 8.313/91) é um dos principais mecanismos de fomento à cultura no Brasil. 
                Para acessar seus benefícios, organizações culturais precisam estar devidamente regularizadas.</p>
                
                <h2>Documentação Necessária</h2>
                <ul>
                    <li>Estatuto social atualizado</li>
                    <li>Ata de eleição da diretoria vigente</li>
                    <li>Comprovantes de regularidade fiscal</li>
                    <li>Certificado de Entidade de Fins Filantrópicos (quando aplicável)</li>
                </ul>
                
                <h2>Assessoria Jurídica Especializada</h2>
                <p>O processo pode ser complexo, especialmente para movimentos sociais e organizações menores. 
                Uma assessoria jurídica especializada garante que seu projeto cultural tenha acesso aos recursos necessários.</p>
            """
        },
        {
            "title": "Superendividamento: A Lei que Protege o Consumidor",
            "slug": "superendividamento-lei-protecao",
            "category": cat_map.get("consumidor"),
            "summary": "A Lei do Superendividamento oferece ferramentas para reorganização financeira e preservação da dignidade.",
            "content": """
                <h2>O que é Superendividamento?</h2>
                <p>É a impossibilidade manifesta de o consumidor, pessoa natural, pagar a totalidade de suas dívidas 
                de consumo, sem comprometer seu mínimo existencial.</p>
                
                <h2>Lei nº 14.181/2021</h2>
                <p>A chamada "Lei do Superendividamento" alterou o Código de Defesa do Consumidor para criar 
                mecanismos de prevenção e tratamento do superendividamento.</p>
                
                <h2>Seus Direitos</h2>
                <ul>
                    <li>Repactuação de dívidas preservando o mínimo existencial</li>
                    <li>Audiências de conciliação obrigatórias</li>
                    <li>Suspensão de cobranças durante negociação</li>
                    <li>Plano de pagamento compatível com a renda</li>
                </ul>
                
                <p><strong>A dignidade da pessoa humana não pode ser sacrificada pelo endividamento. 
                Procure seus direitos.</strong></p>
            """
        },
        {
            "title": "Terceiro Setor: Assessoria para ONGs e Fundações",
            "slug": "terceiro-setor-assessoria-ongs",
            "category": cat_map.get("terceiro-setor"),
            "summary": "Organizações do terceiro setor precisam de suporte jurídico para cumprir sua missão social com segurança.",
            "content": """
                <h2>O Papel do Terceiro Setor</h2>
                <p>ONGs, associações e fundações desempenham papel fundamental na promoção de direitos humanos, 
                proteção ambiental, assistência social e fortalecimento de comunidades.</p>
                
                <h2>Desafios Jurídicos</h2>
                <ul>
                    <li>Regularização estatutária e documental</li>
                    <li>Obtenção de certificações (OSCIP, CEBAS)</li>
                    <li>Compliance e prestação de contas</li>
                    <li>Relações trabalhistas (voluntariado vs. vínculo empregatício)</li>
                    <li>Captação de recursos e parcerias com governo</li>
                </ul>
                
                <h2>Nossa Experiência</h2>
                <p>Com ampla vivência no Terceiro Setor, oferecemos assessoria integral desde a regularização 
                institucional até a consolidação de projetos com aporte governamental.</p>
                
                <p><strong>Se sua organização busca segurança jurídica para seguir transformando realidades, 
                estamos aqui para ajudar.</strong></p>
            """
        }
    ]
    
    created_count = 0
    for data in articles_data:
        article, created = Article.objects.get_or_create(
            slug=data['slug'],
            defaults={
                'title': data['title'],
                'content': data['content'],
                'summary': data['summary'],
                'author': author,
                'is_published': True,
                'published_at': timezone.now()
            }
        )
        
        if created:
            if data.get('category'):
                article.categories.add(data['category'])
            print(f"✅ Created article: {article.title}")
            created_count += 1
        else:
            print(f"⏭️  Article already exists: {article.title}")
    
    return created_count


def main():
    print("=" * 70)
    print("POPULATING INSTITUTIONAL CONTENT - Plataforma Dra. Alessandra Donadon")
    print("=" * 70)
    
    # 1. Get or create author
    print("\n[1/3] Creating author...")
    author = get_or_create_author()
    
    # 2. Create categories
    print("\n[2/3] Creating categories...")
    categories = create_categories()
    
    # 3. Create articles
    print("\n[3/3] Creating articles...")
    created_count = create_articles(author, categories)
    
    print("\n" + "=" * 70)
    print(f"✅ SUCCESS! Created {created_count} articles.")
    print("=" * 70)
    print("\n📌 Next steps:")
    print("   1. Access /admin/ to review content")
    print("   2. Access /in-brief/ to view published articles")
    print("   3. You can now edit articles via Django Admin")
    print()


if __name__ == "__main__":
    main()
