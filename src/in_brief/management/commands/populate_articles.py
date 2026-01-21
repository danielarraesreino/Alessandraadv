from django.core.management.base import BaseCommand
from in_brief.domain.models import Article, Category
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils import timezone
import os

class Command(BaseCommand):
    help = 'Populate In Brief with refined institutional content and images'

    def handle(self, *args, **options):
        User = get_user_model()
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
            author.set_password('admin123')
            author.save()

        # Create Categories
        categories_data = [
            {"name": "Saúde", "slug": "saude"},
            {"name": "Cultural", "slug": "cultural"},
            {"name": "Consumidor", "slug": "consumidor"},
            {"name": "Terceiro Setor", "slug": "terceiro-setor"},
            {"name": "Empresarial", "slug": "empresarial"},
        ]
        
        cat_map = {}
        for data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=data['slug'],
                defaults={'name': data['name']}
            )
            cat_map[data['slug']] = cat

        articles_data = [
            {
                "title": "Lipedema: Direitos do Paciente Frente aos Planos de Saúde",
                "slug": "lipedema-direitos-paciente",
                "category": cat_map.get("saude"),
                "summary": "O lipedema é uma condição crônica que afeta milhões de mulheres. Entenda seus direitos na luta contra negativas de cobertura.",
                "image": "articles/lipedema.png",
                "content": """
                <p>Hoje eu trouxe um tema super atual e de interesse real para quem sofre com <strong>LIPEDEMA</strong>.</p>
                <p>O plano de saúde não pode ignorar a gravidade do lipedema. Negar cirurgia ou tratamento adequado pode configurar prática abusiva!</p>
                <p>Muitas pacientes se sentem desamparadas ao ouvir ‘não’ do plano de saúde. A boa notícia é que a Justiça tem reconhecido esse direito e garantido os tratamentos necessários.</p>
                <p>Quer entender melhor seu caso? Fale comigo.</p>
                """
            },
            {
                "title": "Lei Rouanet: o que você precisa saber (e talvez ainda não saiba)!",
                "slug": "lei-rouanet-regularizacao",
                "category": cat_map.get("cultural"),
                "summary": "Muitos coletivos e associações não acessam recursos por irregularidade documental. Saiba como se regularizar.",
                "image": "articles/rouanet.png",
                "content": """
                <p>Muito se fala em “mamata”, mas por favor, a Lei Rouanet não dá dinheiro a artistas milionários. Ela apenas permite que empresas e pessoas físicas destinem parte do imposto devido para financiar projetos culturais.</p>
                <p>O problema é que muitos coletivos, movimentos sociais, associações, entre outros, não conseguem acessar esses recursos porque estão com a documentação irregular: estatuto desatualizado, atas não registradas, diretoria vencida, CNPJ irregular, e por aí vai.</p>
                <p>Para inscrever projetos culturais é fundamental estar em dia juridicamente. Eu auxilio associações, coletivos e entidades a regularizar a parte documental e, assim, participar de editais e leis de incentivo.</p>
                """
            },
            {
                "title": "Recuperar Valores de Golpes Bancários: Um Direito do Consumidor!",
                "slug": "golpes-bancarios-direitos",
                "category": cat_map.get("consumidor"),
                "summary": "Vítimas de golpes bancários têm direitos. Em muitos casos, os bancos são obrigados a devolver o dinheiro.",
                "image": "articles/golpes.png",
                "content": """
                <p>Cada vez mais pessoas têm sido vítimas de golpes bancários, perdendo economias construídas com muito esforço, seja por transferências indevidas, clonagem de cartão, sequestro de conta ou falsas centrais de atendimento.</p>
                <p>O que nem todos sabem é que, em muitos casos, os bancos são obrigados a devolver o dinheiro, já que têm responsabilidade pela segurança de seus sistemas, conforme prevê o Código de Defesa do Consumidor e a jurisprudência do STJ.</p>
                <p>Lutar contra esses abusos é também lutar por um sistema financeiro mais justo. A grande maioria das pessoas que perde dinheiro em fraudes bancárias fica com vergonha de buscar ajuda. Mas não se culpe: os bancos têm responsabilidade.</p>
                """
            },
            {
                "title": "Alguém aqui está enroscado com o PRONAMPE?",
                "slug": "pronampe-solucoes-juridicas",
                "category": cat_map.get("empresarial"),
                "summary": "O PRONAMPE ajudou muitos negócios, mas também trouxe dívidas difíceis de administrar. Saiba como proteger sua empresa.",
                "image": "articles/pronampe.png",
                "content": """
                <p>O PRONAMPE surgiu como uma promessa de auxílio às micro e pequenas empresas no enfrentamento da crise econômica, mas também trouxe dívidas difíceis de administrar.</p>
                <p>Tem uma jogada quase imperceptível aí, que está fazendo com que os bancos encham ainda os “bolsinhos”! Se você está sofrendo execução judicial, atrasado com parcelas, ou querendo reaver possíveis valores pagos a maior, nós podemos ajudar.</p>
                <p>Podemos te ajudar a proteger sua empresa e encontrar a melhor solução jurídica.</p>
                """
            },
            {
                "title": "Lei do Superendividamento: Prevenção e Tratamento",
                "slug": "lei-superendividamento-prevencao",
                "category": cat_map.get("consumidor"),
                "summary": "A Lei 14.181/21 protege o consumidor e permite a reorganização de compromissos financeiros.",
                "image": "articles/superendividamento.png",
                "content": """
                <p>Ao contrário do que muita gente pensa, a Lei do Superendividamento não protege apenas quem tem empréstimos consignados. As dívidas que podem ser discutidas são quaisquer compromissos financeiros decorrentes de relação de consumo.</p>
                <p>Se as dívidas estão comprometendo seus rendimentos de forma que está ficando difícil viver, podemos ver se sua situação se enquadra nessa Lei, ou se podemos rever os juros, as garantias, enfim, adequar sua dívida.</p>
                """
            },
            {
                "title": "O Plano de Saúde está te dando dor de cabeça?",
                "slug": "direitos-saude-medico",
                "category": cat_map.get("saude"),
                "summary": "Não liberação de exames, reajustes abusivos ou falta de medicamentos do SUS? Entenda seus direitos.",
                "image": "articles/direito_saude.png",
                "content": """
                <p>Seu plano de saúde não libera o exame ou tratamento que seu médico recomendou? O reajuste veio acima do esperado? Estão cobrando multa por cancelamento? E o SUS que era para fornecer aquele medicamento, e até agora, nada?</p>
                <p>Se estiver precisando de uma ajudinha jurídica em Direito da Saúde ou Direito Médico, podem falar comigo, sou advogada especialista na área. Eu posso ver se o seu convênio está agindo correto ou não.</p>
                """
            }
        ]

        for data in articles_data:
            article, created = Article.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'content': data['content'],
                    'summary': data['summary'],
                    'author': author,
                    'image': data['image'],
                    'is_published': True,
                    'published_at': timezone.now()
                }
            )
            
            if data.get('category'):
                article.categories.add(data['category'])
            self.stdout.write(self.style.SUCCESS(f'Updated/Created article: {article.title}'))
