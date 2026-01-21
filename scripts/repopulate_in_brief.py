
import os
import django
from django.utils.text import slugify
from django.core.files import File
from django.contrib.auth import get_user_model

# Setup Django environment
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from in_brief.models import Article, Category

def parse_articles(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by double newlines or some delimiter. 
    # Based on file view, it seems distinct blocks.
    # Pattern: Title is first line. End is "https://wa.me/..." or similar links.
    
    # Rough split by "Sou Alessandra M. Donadon" as a marker of end of body?
    # Actually, the file has blank lines. Let's inspect the structure again.
    # It has 6 clear sections.
    
    raw_articles = content.split('\n\n\n') # Trying to split by multiple newlines if present
    
    if len(raw_articles) < 5:
        # Fallback: split by "Sou Alessandra M. Donadon" to separate articles?
        # The file view showed 63 lines. 
        # Line 4: Title. Line 32: "Sou Alessandra..."
        pass

    # Manual extraction based on known titles or structure would be safer
    return [
        {
            "title": "Lei Rouanet: o que você precisa saber (e talvez ainda não saiba)!",
            "content_lines": [
                "Muito se fala em “mamata”, mas por favor, a Lei Rouanet não dá dinheiro a artistas milionários.",
                "Ela apenas permite que empresas e pessoas físicas destinem parte do imposto devido para financiar projetos culturais.",
                "O problema é que muitos coletivos, movimentos sociais, associações, entre outros, não conseguem acessar esses recursos porque estão com a documentação irregular: estatuto desatualizado, atas não registradas, diretoria vencida, CNPJ irregular, e por aí vai.",
                "Para inscrever projetos culturais é fundamental estar em dia juridicamente.",
                "Eu auxilio associações, coletivos e entidades a regularizar a parte documental e, assim, participar de editais e leis de incentivo.",
            ],
            "category": "Third Sector"
        },
        {
            "title": "RECUPERAR VALORES DE GOLPES BANCÁRIOS: UM DIREITO DO CONSUMIDOR!",
            "content_lines": [
                "Cada vez mais pessoas têm sido vítimas de golpes bancários, perdendo economias construídas com muito esforço.",
                "O que nem todos sabem é que, em muitos casos, os bancos são obrigados a devolver o dinheiro, já que têm responsabilidade pela segurança de seus sistemas.",
                "Apesar disso, as instituições financeiras tentam transferir a culpa para a vítima.",
                "Lutar contra esses abusos é também lutar por um sistema financeiro mais justo.",
                "A grande maioria das pessoas que perde dinheiro em fraudes bancárias fica com vergonha de buscar ajuda. Mas não se culpe: os bancos têm responsabilidade."
            ],
            "category": "Consumer Rights"
        },
        {
            "title": "LIPEDEMA: O plano de saúde não pode ignorar",
            "content_lines": [
                "Hoje eu trouxe um tema super atual e de interesse real para quem sofre com LIPEDEMA.",
                "O plano de saúde não pode ignorar a gravidade do lipedema.",
                "Negar cirurgia ou tratamento adequado pode configurar prática abusiva!",
                "Muitas pacientes se sentem desamparadas ao ouvir ‘não’ do plano de saúde.",
                "A boa notícia é que a Justiça tem reconhecido esse direito e garantido os tratamentos necessários."
            ],
             "category": "Health Law"
        },
        {
            "title": "Alguém aqui está enroscado com o PRONAMPE???",
            "content_lines": [
                "O PRONAMPE, instituído pelo governo federal em 2020, surgiu como uma promessa de auxílio às micro e pequenas empresas.",
                "Mas.......... Porém.... Contudo.... Todavia......",
                "Certo que ajudou muitos negócios, mas também trouxe dívidas difíceis de administrar.",
                "Tem uma jogada quase imperceptível aí, que está fazendo com que os bancos encham ainda os “bolsinhos”!",
                "Se você está sofrendo execução judicial ou precisando renegociar, nós podemos te ajudar."
            ],
            "category": "Business Law"
        },
        {
            "title": "Lei do Superendividamento: Prevenção e Tratamento",
            "content_lines": [
                "Hoje vim falar de um assunto que interessa muita gente - a Lei 14.181/21 - que trata da prevenção e o tratamento do superendividamento.",
                "Ao contrário do que muita gente pensa, a Lei do Superendividamento não protege apenas quem tem empréstimos consignados.",
                "As dívidas que podem ser discutidas são quaisquer compromissos financeiros assumidos decorrentes de relação de consumo.",
                "A verdade é que não está fácil para ninguém!!! Mas saiba que se as dívidas então comprometendo seus rendimentos, podemos rever os juros."
            ],
            "category": "Consumer Rights"
        },
        {
            "title": "Direito da Saúde: Problemas com o Plano?",
            "content_lines": [
                "Olá canhotos! Me contem, seu plano de saúde está te dando dor de cabeça?",
                "Não libera o exame ou tratamento que seu médico recomendou? O reajuste veio acima do esperado?",
                "Se estiver precisando de uma ajudinha jurídica em Direito da Saúde ou Direito Médico, podem falar comigo, sou advogada especialista na área."
            ],
             "category": "Health Law"
        }
    ]

def run():
    User = get_user_model()
    # Ensure we have a user
    author = User.objects.first()
    if not author:
        print("Creating superuser...")
        author = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')

    articles_data = parse_articles('textos_extracted.txt')

    print(f"Found {len(articles_data)} articles to create/update.")

    for data in articles_data:
        # Get or create category
        cat_slug = slugify(data['category'])
        category, _ = Category.objects.get_or_create(name=data['category'], defaults={'slug': cat_slug})

        # Create Article
        title = data['title']
        slug = slugify(title)
        content_html = "<p>" + "</p><p>".join(data['content_lines']) + "</p>"
        summary = data['content_lines'][0] if data['content_lines'] else ""
        
        # Check if exists
        article, created = Article.objects.update_or_create(
            slug=slug,
            defaults={
                'title': title,
                'content': content_html,
                'summary': summary,
                'author': author,
                'is_published': True
            }
        )
        article.categories.add(category)
        if created:
            print(f"Created article: {title}")
        else:
            print(f"Updated article: {title}")

if __name__ == "__main__":
    run()
