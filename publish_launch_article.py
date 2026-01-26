
import os
import sys
import django
from django.utils.text import slugify
from django.utils import timezone
from django.core.files import File

# Setup Django environment
sys.path.append(os.path.join(os.getcwd(), 'src'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from in_brief.models import Article, Category
from django.contrib.auth import get_user_model

def publish_article():
    User = get_user_model()
    
    # Ensure Category exists
    category, created = Category.objects.get_or_create(
        name='Inovação & Tecnologia',
        defaults={'slug': 'inovacao-tecnologia'}
    )
    
    # Ensure SUPORTE user exists
    user, created = User.objects.get_or_create(
        username='suporte',
        defaults={
            'first_name': 'Suporte de Inteligência',
            'last_name': '(Desenvolvedor Arraes)',
            'email': 'suporte@alessandradonadon.adv.br'
        }
    )

    title = "Além do Software de Prateleira: Por que a Elite Profissional Exige Soberania Digital"
    slug = slugify("Soberania Digital Elite Profissional") # Stable slug
    
    summary = "O caso Dra. Alessandra Donadon: Como transformamos a exigência extrema por segurança em um ativo digital proprietário."
    
    content = """
    <p style="font-size: 1.1rem; color: var(--color-gray); margin-bottom: 2rem;">
        <em>Por Daniel Arraes Reino - Arquiteto de Soluções Digitais</em><br>
        26 de Janeiro de 2026
    </p>

    <p>No mercado atual, a maioria dos profissionais aceita o "padrão da indústria": fragmentar os dados vitais de seus clientes em dezenas de softwares de terceiros. É a solução fácil, rápida e, infelizmente, perigosa.</p>

    <p>Quando iniciei o projeto para o escritório da Dra. Alessandra M. Donadon, ficou claro imediatamente que o "padrão" não seria suficiente. A Dra. Alessandra é conhecida por um nível de exigência técnica e ética que não admite concessões. Ela não queria apenas um "site bonito"; ela precisava de um porto seguro digital que refletisse a seriedade de sua prática jurídica.</p>

    <p>Os desafios de atender a um cliente com esse perfil são imensos, mas o resultado redefine o que é possível em tecnologia jurídica. Decidimos trilhar o caminho mais árduo e recompensador: a <strong>Soberania de Dados</strong>.</p>

    <h3>O Perigo da Fragmentação vs. A Força do Ecossistema Próprio</h3>

    <p>Ao usar ferramentas genéricas ("SaaS de prateleira"), seus dados e os segredos de seus clientes residem em servidores compartilhados que você não conhece, sob termos de uso que mudam sem aviso.</p>

    <p>Para este projeto, centralizamos tudo em uma plataforma proprietária. Neste ecossistema, nós controlamos cada bit de informação. Não é um software alugado; é um ativo digital construído sob medida para as necessidades exatas do escritório, resultando em uma estrutura blindada:</p>

    <ul>
        <li><strong>Criptografia de Nível Militar (Encrypted DB):</strong> O banco de dados não é apenas um depósito de informações; é uma fortaleza. Implementamos algoritmos avançados onde, sem a chave mestra, a informação sensível dos clientes é absolutamente ilegível.</li>
        <li><strong>Túnel de Conexão Certificada (SSL Secure):</strong> Cada interação no Portal do Cliente ou no Simulador de Prazos trafega por um túnel criptografado exclusivo, eliminando riscos de interceptação.</li>
        <li><strong>Privacy by Design (LGPD Nativa):</strong> Diferente da maioria dos sistemas que foram "adaptados" às pressas para a LGPD, esta plataforma foi arquitetada sob a égide da lei desde a primeira linha de código. A privacidade não é uma funcionalidade adicional; é a fundação do sistema.</li>
    </ul>

    <h3>A Tecnologia como Diferencial Competitivo</h3>

    <p>Tenho um orgulho imenso da entrega técnica desta solução. Trabalhar com clientes que demandam excelência absoluta nos força a elevar nosso próprio padrão. O resultado — essa interface limpa, intuitiva e extremamente robusta que você vê hoje — é fruto de uma arquitetura pensada para resistir ao tempo e às ameaças modernas.</p>

    <p>Esta plataforma prova que quando o Direito de alto nível encontra a Tecnologia de ponta, a experiëncia do cliente é transformada.</p>

    <p>Meu nome está no rodapé deste projeto como uma assinatura de qualidade. Este é, sem dúvida, um dos sistemas mais seguros, bem estruturados e resilientes que já tive o privilégio de arquitetar.</p>

    <p>Se você é um profissional que entende que os dados do seu negócio não podem ficar reféns de terceiros, precisamos conversar.</p>
    """

    # Cleanup old references if they exist
    Article.objects.filter(slug=slug).delete()
    Article.objects.filter(title__icontains="Soberania Digital").delete()

    # Create the refined article
    article = Article.objects.create(
        slug=slug,
        title=title,
        summary=summary,
        content=content,
        author=user,
        is_published=True,
        published_at=timezone.now()
    )
    
    # Attach image
    image_path = "src/media/articles/soberania_digital.jpg"
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            article.image.save('soberania_digital_vault.jpg', File(f), save=True)

    article.categories.add(category)
    print(f"Artigo '{title}' publicado com sucesso sob o usuário '{user.username}'! ID: {article.id}")

if __name__ == '__main__':
    publish_article()
