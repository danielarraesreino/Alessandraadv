
import os
import sys
import django
from django.db import connection, transaction
from django.core.management import call_command
from django.core.files import File
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

# Setup Django
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from in_brief.models import Article, Category

def check_column_exists(table, column):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = %s AND column_name = %s;",
            [table, column]
        )
        return cursor.fetchone() is not None

def run_fix():
    print("--- STARTING PRODUCTION FIX ---")
    
    # 1. Run Migrations
    print("Running migrations...")
    try:
        call_command("migrate", "in_brief", interactive=False)
        print("Migrate command executed.")
    except Exception as e:
        print(f"Migrate command failed: {e}")

    # 2. Verify Column Existence (and force fix if needed)
    print("Verifying 'image' column in 'in_brief_article'...")
    if not check_column_exists('in_brief_article', 'image'):
        print("WARNING: 'image' column MISSING after migration. Attempting manual fix...")
        try:
            with connection.cursor() as cursor:
                # Add column manually (PostgreSQL syntax)
                cursor.execute('ALTER TABLE in_brief_article ADD COLUMN image varchar(100);')
            print("SUCCESS: Manually added 'image' column.")
        except Exception as e:
            print(f"CRITICAL: Failed to manually add column: {e}")
            # We might continue, but expect errors
    else:
        print("SUCCESS: 'image' column exists.")

    # 3. Populate Content & Images
    populate_content()

def populate_content():
    print("Populating content...")
    User = get_user_model()
    author = User.objects.filter(is_superuser=True).first()
    if not author:
        print("Creating superuser...")
        author = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        
    print(f"Using author: {author.username}")

    # Define Articles Data using the hardcoded list from previous context
    # We assign distinct image filenames where we have them.
    articles_data = [
        {
            "title": "Lei Rouanet: o que você precisa saber (e talvez ainda não saiba)!",
            "slug": "lei-rouanet-regularizacao", 
            "category": "Third Sector", # "Terceiro Setor" in PT
            "image_filename": "rouanet.png",
            "summary": "Muitos coletivos e associações não acessam recursos por irregularidade documental. Saiba como se regularizar.",
            "content": """
                <p>Muito se fala em “mamata”, mas por favor, a Lei Rouanet não dá dinheiro a artistas milionários.</p>
                <p>Ela apenas permite que empresas e pessoas físicas destinem parte do imposto devido para financiar projetos culturais.</p>
                <p>O problema é que muitos coletivos, movimentos sociais, associações, entre outros, não conseguem acessar esses recursos porque estão com a documentação irregular: estatuto desatualizado, atas não registradas, diretoria vencida, CNPJ irregular, e por aí vai.</p>
                <p>Para inscrever projetos culturais é fundamental estar em dia juridicamente.</p>
                <p>Eu auxilio associações, coletivos e entidades a regularizar a parte documental e, assim, participar de editais e leis de incentivo.</p>
            """
        },
        {
            "title": "RECUPERAR VALORES DE GOLPES BANCÁRIOS: UM DIREITO DO CONSUMIDOR!",
            "slug": "golpes-bancarios-direitos",
            "category": "Consumer Rights",
            "image_filename": "golpes.png",
            "summary": "Vítimas de golpes bancários têm direitos. Em muitos casos, os bancos são obrigados a devolver o dinheiro.",
            "content": """
                <p>Cada vez mais pessoas têm sido vítimas de golpes bancários, perdendo economias construídas com muito esforço.</p>
                <p>O que nem todos sabem é que, em muitos casos, os bancos são obrigados a devolver o dinheiro, já que têm responsabilidade pela segurança de seus sistemas.</p>
                <p>Apesar disso, as instituições financeiras tentam transferir a culpa para a vítima.</p>
                <p>Lutar contra esses abusos é também lutar por um sistema financeiro mais justo.</p>
                <p>A grande maioria das pessoas que perde dinheiro em fraudes bancárias fica com vergonha de buscar ajuda. Mas não se culpe: os bancos têm responsabilidade.</p>
            """
        },
        {
            "title": "LIPEDEMA: O plano de saúde não pode ignorar",
            "slug": "lipedema-direitos-paciente",
            "category": "Health Law",
            "image_filename": "lipedema.png",
            "summary": "O plano de saúde não pode ignorar a gravidade do lipedema. Negar cirurgia ou tratamento adequado pode configurar prática abusiva!",
            "content": """
                <p>Hoje eu trouxe um tema super atual e de interesse real para quem sofre com LIPEDEMA.</p>
                <p>O plano de saúde não pode ignorar a gravidade do lipedema.</p>
                <p>Negar cirurgia ou tratamento adequado pode configurar prática abusiva!</p>
                <p>Muitas pacientes se sentem desamparadas ao ouvir ‘não’ do plano de saúde.</p>
                <p>A boa notícia é que a Justiça tem reconhecido esse direito e garantido os tratamentos necessários.</p>
            """
        },
        {
            "title": "Alguém aqui está enroscado com o PRONAMPE???",
            "slug": "pronampe-solucoes",
            "category": "Business Law",
            "image_filename": "pronampe.png",  # Placeholder if not exists, script handles missing img gracefully
            "summary": "O PRONAMPE ajudou muitos negócios, mas também trouxe dívidas difíceis de administrar.",
            "content": """
                <p>O PRONAMPE, instituído pelo governo federal em 2020, surgiu como uma promessa de auxílio às micro e pequenas empresas.</p>
                <p>Mas.......... Porém.... Contudo.... Todavia......</p>
                <p>Certo que ajudou muitos negócios, mas também trouxe dívidas difíceis de administrar.</p>
                <p>Tem uma jogada quase imperceptível aí, que está fazendo com que os bancos encham ainda os “bolsinhos”!</p>
                <p>Se você está sofrendo execução judicial ou precisando renegociar, nós podemos te ajudar.</p>
            """
        },
        {
            "title": "Lei do Superendividamento: Prevenção e Tratamento",
            "slug": "lei-superendividamento",
            "category": "Consumer Rights",
            "image_filename": "superendividamento.png",
            "summary": "A Lei do Superendividamento não protege apenas quem tem empréstimos consignados. Saiba mais.",
            "content": """
                <p>Hoje vim falar de um assunto que interessa muita gente - a Lei 14.181/21 - que trata da prevenção e o tratamento do superendividamento.</p>
                <p>Ao contrário do que muita gente pensa, a Lei do Superendividamento não protege apenas quem tem empréstimos consignados.</p>
                <p>As dívidas que podem ser discutidas são quaisquer compromissos financeiros assumidos decorrentes de relação de consumo.</p>
                <p>A verdade é que não está fácil para ninguém!!! Mas saiba que se as dívidas então comprometendo seus rendimentos, podemos rever os juros.</p>
            """
        },
        {
            "title": "Direito da Saúde: Problemas com o Plano?",
            "slug": "problemas-plano-saude",
            "category": "Health Law",
            "image_filename": "direito_saude.png",
            "summary": "Não libera o exame ou tratamento que seu médico recomendou? O reajuste veio acima do esperado?",
            "content": """
                <p>Olá canhotos! Me contem, seu plano de saúde está te dando dor de cabeça?</p>
                <p>Não libera o exame ou tratamento que seu médico recomendou? O reajuste veio acima do esperado?</p>
                <p>Se estiver precisando de uma ajudinha jurídica em Direito da Saúde ou Direito Médico, podem falar comigo, sou advogada especialista na área.</p>
            """
        }
    ]

    for data in articles_data:
        # Use explicit slug if provided, else slugify title
        slug = data.get('slug') or slugify(data['title'])
        print(f"Processing Article: {slug}")
        
        # Category
        cat_name = data['category']
        cat_slug = slugify(cat_name)
        category, _ = Category.objects.get_or_create(name=cat_name, defaults={'slug': cat_slug})

        # Update/Create Article
        article, created = Article.objects.update_or_create(
            slug=slug,
            defaults={
                'title': data['title'],
                'content': data['content'],
                'summary': data['summary'],
                'author': author,
                'is_published': True,
                'published_at': timezone.now()
            }
        )
        article.categories.add(category)

        # Image
        img_name = data.get('image_filename')
        if img_name:
            # Try finding image
            base_dir = os.path.dirname(__file__)
            path1 = os.path.join(base_dir, f"../src/core/static/images/articles/{img_name}")
            path2 = os.path.join(base_dir, f"../media/articles/{img_name}")
            
            p = path1 if os.path.exists(path1) else path2 if os.path.exists(path2) else None
            
            if p:
                with open(p, 'rb') as f:
                    article.image.save(img_name, File(f), save=True)
                print(f"  -> Image assigned: {img_name}")
            else:
                print(f"  -> WARNING: Image {img_name} not found locally.")
                
    print("--- PRODUCTION FIX COMPLETED ---")

if __name__ == "__main__":
    run_fix()
