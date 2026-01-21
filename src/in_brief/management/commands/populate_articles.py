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
                "summary": "O plano de saúde não pode ignorar a gravidade do lipedema. Negar cirurgia ou tratamento adequado pode configurar prática abusiva!",
                "image": "articles/lipedema.png",
                "content": """
                <p>Hoje eu trouxe um tema super atual e de interesse real para quem sofre com <strong>LIPEDEMA</strong>.</p>
                <p>O plano de saúde não pode ignorar a gravidade do lipedema. Negar cirurgia ou tratamento adequado pode configurar prática abusiva!</p>
                <p>Muitas pacientes se sentem desamparadas ao ouvir ‘não’ do plano de saúde. A boa notícia é que a Justiça tem reconhecido esse direito e garantido os tratamentos necessários.</p>
                <p>Quer entender melhor seu caso? Fale comigo.</p>
                <p>Sou Alessandra M. Donadon, advogada inscrita na OAB/SP 165/917, formada em 1998 pela Universidade São Francisco.</p>
                <p>Você pode me contatar através do link abaixo:<br><a href="https://wa.me/+5519988014465">https://wa.me/+5519988014465</a></p>
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
                <p>Para inscrever projetos culturais é fundamental estar em dia juridicamente.</p>
                <p>Eu auxilio associações, coletivos e entidades a regularizar a parte documental e, assim, participar de editais e leis de incentivo.</p>
                <p>Me chama no privado que eu explico como funciona.</p>
                <p>Sou Alessandra M. Donadon, advogada inscrita na OAB/SP 165/917, formada em 1998 pela Universidade São Francisco. Atualmente, sou Secretária da Comissão do Terceiro Setor da OAB Campinas.</p>
                <p>Você pode me contatar através dos links abaixo:<br><a href="https://wa.me/+5519988014465">https://wa.me/+5519988014465</a></p>
                """
            },
            {
                "title": "Recuperar Valores de Golpes Bancários: Um Direito do Consumidor!",
                "slug": "golpes-bancarios-direitos",
                "category": cat_map.get("consumidor"),
                "summary": "Vítimas de golpes bancários têm direitos. Em muitos casos, os bancos são obrigados a devolver o dinheiro.",
                "image": "articles/golpes.png",
                "content": """
                <p>Cada vez mais pessoas têm sido vítimas de golpes bancários, perdendo economias construídas com muito esforço, seja por transferências indevidas, clonagem de cartão, sequestro de conta ou falsas centrais de atendimento, golpe do falso advogado, do falso processo, do falso boleto, "golpe PIX", entre tantos outros, e o pior - cada dia aparece um novo.</p>
                <p>O que nem todos sabem é que, <strong>em muitos casos, os bancos são obrigados a devolver o dinheiro</strong>, já que têm responsabilidade pela segurança de seus sistemas, conforme prevê o Código de Defesa do Consumidor e a jurisprudência do STJ.</p>
                <p>Apesar disso, as instituições financeiras tentam transferir a culpa para a vítima, alegando descuido ou imprudência. Essa prática é injusta e inaceitável, pois coloca o consumidor em desvantagem diante de conglomerados bilionários.</p>
                <p>Lutar contra esses abusos é também lutar por um sistema financeiro mais justo, em que a vida e o trabalho das pessoas valham mais do que os lucros dos bancos.</p>
                <p>A grande maioria das pessoas que perde dinheiro em fraudes bancárias fica com vergonha de buscar ajuda. Mas não se culpe: os bancos têm responsabilidade pela segurança de suas operações e, em muitos casos, são obrigados a devolver o valor.</p>
                <p>Garanto sigilo absoluto na consulta, porque sabemos o quanto essa situação causa constrangimento.</p>
                <p>Sou Alessandra M. Donadon, advogada inscrita na OAB/SP 165/917, formada em 1998 pela Universidade São Francisco.</p>
                <p>Você pode me contatar através dos links abaixo:<br><a href="https://wa.me/+5519988014465">https://wa.me/+5519988014465</a></p>
                """
            },
            {
                "title": "Alguém aqui está enroscado com o PRONAMPE?",
                "slug": "pronampe-solucoes-juridicas",
                "category": cat_map.get("empresarial"),
                "summary": "O PRONAMPE ajudou muitos negócios, mas também trouxe dívidas difíceis de administrar. Saiba como proteger sua empresa.",
                "image": "articles/pronampe.png",
                "content": """
                <p>O PRONAMPE, instituído pelo governo federal em 2020 por meio da Lei nº 13.999/20, surgiu como uma promessa de auxílio às micro e pequenas empresas no enfrentamento da crise econômica causada pela pandemia, e veio se consolidando como excelente alternativa bancária.</p>
                <p>Mas.......... Porém.... Contudo.... Todavia......</p>
                <p>Certo que ajudou muitos negócios, mas também trouxe dívidas difíceis de administrar, e falando a real, muito provavelmente quem quitou, pagou a mais.</p>
                <p>Tem uma jogada quase imperceptível aí, que está fazendo com que os bancos encham ainda os “bolsinhos”!</p>
                <p>Se você está:
                <ul>
                    <li>Sofrendo execução judicial,</li>
                    <li>Atrasado com parcelas,</li>
                    <li>Querendo reaver possíveis valores pagos a maior;</li>
                    <li>Ou precisando renegociar seu contrato...</li>
                </ul>
                </p>
                <p>Nós podemos te ajudar a proteger sua empresa e encontrar a melhor solução jurídica.</p>
                <p>Sou Alessandra M. Donadon, advogada inscrita na OAB/SP 165/917, formada em 1998 pela Universidade São Francisco.</p>
                <p>Você pode me contatar através dos links abaixo:</p>
                """
            },
            {
                "title": "Lei do Superendividamento: Prevenção e Tratamento",
                "slug": "lei-superendividamento-prevencao",
                "category": cat_map.get("consumidor"),
                "summary": "A Lei 14.181/21 protege o consumidor e permite a reorganização de compromissos financeiros.",
                "image": "articles/superendividamento.png",
                "content": """
                <p>Hoje vim falar de um assunto que interessa muita gente - a Lei 14.181/21 - que trata da prevenção e o tratamento do superendividamento.</p>
                <p>Ao contrário do que muita gente pensa, a Lei do Superendividamento não protege apenas quem tem empréstimos consignados.</p>
                <p>As dívidas que podem ser discutidas são “quaisquer compromissos financeiros assumidos decorrentes de relação de consumo, inclusive operações de crédito, compras a prazo e serviços de prestação continuada.”</p>
                <p>A verdade é que não está fácil para ninguém!!! Mas saiba que se as dívidas então comprometendo seus rendimentos de forma que está ficando difícil viver, podemos ver se sua situação se enquadra nessa Lei, ou se podemos rever os juros, as garantias, enfim, adequar sua dívida.</p>
                <p>Sou Alessandra Donadon, advogada inscrita na OAB/SP 165.917, e será um prazer te ajudar nesse ou em outros assuntos.</p>
                <p>Me chame no whatsapp (19) 98801.4465 ou pelo link</p>
                """
            },
            {
                "title": "O Plano de Saúde está te dando dor de cabeça?",
                "slug": "direitos-saude-medico",
                "category": cat_map.get("saude"),
                "summary": "Não liberação de exames, reajustes abusivos ou falta de medicamentos do SUS? Entenda seus direitos.",
                "image": "articles/direito_saude.png",
                "content": """
                <p>Olá canhotos!</p>
                <p>Me contem, seu plano de saúde está te dando dor de cabeça? Não libera o exame ou tratamento que seu médico recomendou? O reajuste veio acima do esperado? Estão cobrando multa por cancelamento? E o SUS que era para fornecer aquele medicamento, e até agora, nada?</p>
                <p>Se estiver precisando de uma ajudinha jurídica em Direito da Saúde ou Direito Médico, podem falar comigo, sou advogada especialista na área, inscrita na OAB/SP 165.917. Eu posso ver se o seu convênio está agindo correto ou não... Podem me chamar por aqui ou pelo zapzap (19) 98801-4465</p>
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
