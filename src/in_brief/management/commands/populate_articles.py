from django.core.management.base import BaseCommand
from in_brief.models import Article
from django.core.files import File
from django.conf import settings
import os
from datetime import datetime
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Populates In Brief articles with content and images'

    def handle(self, *args, **options):
        User = get_user_model()
        author = User.objects.first()
        if not author:
            self.stdout.write("No user found. Creating admin user.")
            author = User.objects.create_superuser('admin', 'admin@example.com', 'admin')

        articles_data = [
            {
                'slug': 'lei-rouanet',
                'title': 'Lei Rouanet: o que você precisa saber (e talvez ainda não saiba)!',
                'summary': 'Muito se fala em “mamata”, mas por favor, a Lei Rouanet não dá dinheiro a artistas milionários. Ela apenas permite que empresas e pessoas físicas destinem parte do imposto devido para financiar projetos culturais.',
                'content': """Muito se fala em “mamata”, mas por favor, a Lei Rouanet não dá dinheiro a artistas milionários. Ela apenas permite que empresas e pessoas físicas destinem parte do imposto devido para financiar projetos culturais.
O problema é que muitos coletivos, movimentos sociais, associações, entre outros, não conseguem acessar esses recursos porque estão com a documentação irregular: estatuto desatualizado, atas não registradas, diretoria vencida, CNPJ irregular, e por aí vai.
Para inscrever projetos culturais é fundamental estar em dia juridicamente.
Eu auxilio associações, coletivos e entidades a regularizar a parte documental e, assim, participar de editais e leis de incentivo.
Me chama no privado que eu explico como funciona.
Sou Alessandra M. Donadon, advogada inscrita na OAB/SP 165/917, formada em 1998 pela Universidade São Francisco. Atualmente, sou Secretária da Comissão do Terceiro Setor da OAB Campinas.
Você pode me contatar através dos links abaixo:
https://wa.me/+5519988014465""",
                'image_filename': 'lei_rouanet.png'
            },
            {
                'slug': 'golpes-bancarios',
                'title': 'RECUPERAR VALORES DE GOLPES BANCÁRIOS: UM DIREITO DO CONSUMIDOR!',
                'summary': 'Cada vez mais pessoas têm sido vítimas de golpes bancários, perdendo economias construídas com muito esforço. Saiba que, em muitos casos, os bancos são obrigados a devolver o dinheiro.',
                'content': """Cada vez mais pessoas têm sido vítimas de golpes bancários, perdendo economias construídas com muito esforço, seja por transferências indevidas, clonagem de cartão, sequestro de conta ou falsas centrais de atendimento, golpe do falso advogado, do falso processo, do falso boleto, "golpe PIX", entre tantos outros, e o pior - cada dia aparece um novo.
O que nem todos sabem é que, em muitos casos, os bancos são obrigados a devolver o dinheiro, já que têm responsabilidade pela segurança de seus sistemas, conforme prevê o Código de Defesa do Consumidor e a jurisprudência do STJ.
Apesar disso, as instituições financeiras tentam transferir a culpa para a vítima, alegando descuido ou imprudência. Essa prática é injusta e inaceitável, pois coloca o consumidor em desvantagem diante de conglomerados bilionários.
Lutar contra esses abusos é também lutar por um sistema financeiro mais justo, em que a vida e o trabalho das pessoas valham mais do que os lucros dos bancos.
A grande maioria das pessoas que perde dinheiro em fraudes bancárias fica com vergonha de buscar ajuda. Mas não se culpe: os bancos têm responsabilidade pela segurança de suas operações e, em muitos casos, são obrigados a devolver o valor.
Garanto sigilo absoluto na consulta, porque sabemos o quanto essa situação causa constrangimento.
Sou Alessandra M. Donadon, advogada inscrita na OAB/SP 165/917, formada em 1998 pela Universidade São Francisco.
Você pode me contatar através dos links abaixo:
https://wa.me/+5519988014465""",
                'image_filename': 'golpes_bancarios.png'
            },
            {
                'slug': 'lipedema',
                'title': 'LIPEDEMA: O plano de saúde não pode ignorar',
                'summary': 'Hoje eu trouxe um tema super atual e de interesse real para quem sofre com LIPEDEMA. O plano de saúde não pode ignorar a gravidade do lipedema. Negar cirurgia ou tratamento adequado pode configurar prática abusiva!',
                'content': """Hoje eu trouxe um tema super atual e de interesse real para quem sofre com LIPEDEMA.
O plano de saúde não pode ignorar a gravidade do lipedema.
Negar cirurgia ou tratamento adequado pode configurar prática abusiva!
Muitas pacientes se sentem desamparadas ao ouvir ‘não’ do plano de saúde.
A boa notícia é que a Justiça tem reconhecido esse direito e garantido os tratamentos necessários.
Quer entender melhor seu caso? Fale comigo
Sou Alessandra M. Donadon, advogada inscrita na OAB/SP 165/917, formada em 1998 pela Universidade São Francisco.
Você pode me contatar através do link abaixo:
https://wa.me/+5519988014465""",
                'image_filename': 'lipedema.png'
            },
            {
                'slug': 'pronampe',
                'title': 'PRONAMPE: Solução ou armadilha?',
                'summary': 'Alguém aqui está enroscado com o PRONAMPE??? Certo que ajudou muitos negócios, mas também trouxe dívidas difíceis de administrar.',
                'content': """Alguém aqui está enroscado com o PRONAMPE???
O PRONAMPE, instituído pelo governo federal em 2020 por meio da Lei nº 13.999/20, surgiu como uma promessa de auxílio às micro e pequenas empresas no enfrentamento da crise econômica causada pela pandemia, e veio se consolidando como excelente alternativa bancária.
Mas.......... Porém.... Contudo.... Todavia......
Certo que ajudou muitos negócios, mas também trouxe dívidas difíceis de administrar, e falando a real, muito provavelmente quem quitou, pagou a mais.
Tem uma jogada quase imperceptível aí, que está fazendo com que os bancos encham ainda os “bolsinhos”!
Se você está:
• Sofrendo execução judicial,
• Atrasado com parcelas,
• Querendo reaver possíveis valores pagos a maior;
• Ou precisando renegociar seu contrato...
Nós podemos te ajudar a proteger sua empresa e encontrar a melhor solução jurídica.
Sou Alessandra M. Donadon, advogada inscrita na OAB/SP 165/917, formada em 1998 pela Universidade São Francisco.
Você pode me contatar através dos links abaixo:""",
                'image_filename': 'pronampe.png'
            },
            {
                'slug': 'superendividamento',
                'title': 'Lei do Superendividamento: Uma saída possível',
                'summary': 'Hoje vim falar de um assunto que interessa muita gente - a Lei 14.181/21 - que trata da prevenção e o tratamento do superendividamento.',
                'content': """Hoje vim falar de um assunto que interessa muita gente - a Lei 14.181/21 - que trata da prevenção e o tratamento do superendividamento.
Ao contrário do que muita gente pensa, a Lei do Superendividamento não protege apenas quem tem empréstimos consignados.
As dívidas que podem ser discutidas são “quaisquer compromissos financeiros assumidos decorrentes de relação de consumo, inclusive operações de crédito, compras a prazo e serviços de prestação continuada.”
A verdade é que não está fácil para ninguém!!! Mas saiba que se as dívidas então comprometendo seus rendimentos de forma que está ficando difícil viver, podemos ver se sua situação se enquadra nessa Lei, ou se podemos rever os juros, as garantias, enfim, adequar sua dívida.
Sou Alessandra Donadon, advogada inscrita na OAB/SP 165.917, e será um prazer te ajudar nesse ou em outros assuntos.
Me chame no whatsapp (19) 98801.4465 ou pelo link""",
                'image_filename': 'superendividamento.png'
            },
            {
                'slug': 'direito-saude',
                'title': 'Problemas com Plano de Saúde? Saiba seus direitos',
                'summary': 'Me contem, seu plano de saúde está te dando dor de cabeça? Não libera o exame ou tratamento que seu médico recomendou?',
                'content': """Olá canhotos!
Me contem, seu plano de saúde está te dando dor de cabeça? Não libera o exame ou tratamento que seu médico recomendou? O reajuste veio acima do esperado? Estão cobrando multa por cancelamento? E o SUS que era para fornecer aquele medicamento, e até agora, nada?
Se estiver precisando de uma ajudinha jurídica em Direito da Saúde ou Direito Médico, podem falar comigo, sou advogada especialista na área, inscrita na OAB/SP 165.917. Eu posso ver se o seu convênio está agindo correto ou não... Podem me chamar por aqui ou pelo zapzap (19) 98801-4465""",
                'image_filename': 'direito_saude.png'
            }
        ]

        # Ensure media directory exists
        media_root = settings.MEDIA_ROOT
        articles_media_dir = os.path.join(media_root, 'articles')
        os.makedirs(articles_media_dir, exist_ok=True)

        for data in articles_data:
            self.stdout.write(f"Processing article: {data['slug']}")
            
            defaults = {
                'title': data['title'],
                'content': data['content'],
                'summary': data['summary'],
                'is_published': True,
                'published_at': datetime.now(),
                'author': author,
            }

            article, created = Article.objects.get_or_create(
                slug=data['slug'],
                defaults=defaults
            )

            if not created:
                article.title = data['title']
                article.content = data['content']
                article.summary = data['summary']
                article.is_published = True
                article.author = author
                # Don't update published_at if already exists to preserve original date

            # Handle Image
            image_path = os.path.join(articles_media_dir, data['image_filename'])
            
            # If image doesn't exist, create a placeholder
            if not os.path.exists(image_path):
                self.stdout.write(f"  Image not found: {image_path}, creating placeholder...")
                try:
                    from PIL import Image, ImageDraw, ImageFont
                    img = Image.new('RGB', (800, 400), color=(10, 25, 47)) # Dark blue/black
                    d = ImageDraw.Draw(img)
                    d.rectangle([(20, 20), (780, 380)], outline="gold", width=5)
                    # Text fallback
                    # d.text((20, 20), data['slug'], fill="white")
                    img.save(image_path)
                except ImportError:
                     self.stdout.write(self.style.WARNING("  PIL not installed, skipping placeholder generation."))

            
            # Open and save to model
            if os.path.exists(image_path):
                 with open(image_path, 'rb') as f:
                    article.image.save(data['image_filename'], File(f), save=True)
            
            article.save()
            self.stdout.write(self.style.SUCCESS(f"  Successfully updated: {article.title}"))

