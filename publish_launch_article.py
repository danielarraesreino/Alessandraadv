
import os
import sys
import django
from django.utils.text import slugify
from django.utils import timezone

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
    if not category.slug:
        category.slug = slugify(category.name)
        category.save()
    
    # Ensure User exists for Daniel
    user, created = User.objects.get_or_create(
        username='daniel',
        defaults={
            'first_name': 'Daniel',
            'last_name': 'Arraes Reino',
            'email': 'daniel@example.com' # Placeholder
        }
    )

    title = "Soberania Digital: Por que a Dra. Alessandra escolheu uma Plataforma Própria e Segura?"
    slug = slugify(title)
    
    summary = "Uma análise técnica e ética sobre como a centralização de dados em um ecossistema proprietário redefine a segurança para o cliente."
    
    content = """
    <p>Neste artigo, falo não apenas como desenvolvedor, mas como alguém que viu de perto o compromisso da Dra. Alessandra M. Donadon com a segurança e o respeito absoluto pelos dados de seus clientes. Quando começamos a desenhar este projeto, a meta era clara: <strong>não ser apenas mais um site, mas um porto seguro digital.</strong></p>

    <p>Ao contrário da maioria, que fragmenta os dados em dezenas de softwares de terceiros, decidimos trilhar o caminho da <strong>Soberania de Dados</strong>. Centralizamos tudo em uma plataforma proprietária, onde nós controlamos cada bit de informação.</p>

    <h3>A Força de um Ecossistema Próprio</h3>
    <p>A fragmentação é o maior risco do mundo moderno. Ao usar ferramentas genéricas de prateleira, seus dados estão em servidores que você não conhece. Aqui, no ecossistema Alessandra M. Donadon, os dados residem em uma estrutura blindada:</p>
    
    <ul>
        <li><strong>Criptografia de Ponta (Encrypted DB):</strong> Implementamos algoritmos que tornam o banco de dados uma fortaleza. Sem a chave certa, a informação é apenas ruído ilegível.</li>
        <li><strong>Conexão Certificada (SSL Secure):</strong> Cada acesso ao Portal do Cliente ou ao Simulador de Prazos é protegido por um túnel criptografado.</li>
        <li><strong>Privacy by Design (LGPD):</strong> Não "adaptamos" o sistema à LGPD; nós o construímos sob a égide da lei desde a primeira linha de código.</li>
    </ul>

    <h3>Orgulho de Ver a Tecnologia Servindo ao Direito</h3>
    <p>Tenho um orgulho imenso de ter desenvolvido esta solução. O resultado que você vê aqui — esta interface limpa, intuitiva e extremamente robusta — é fruto de uma entrega técnica de alto nível. Fomos, sem modéstia, "fodassos" em construir algo que realmente protege a história de cada pessoa que busca este escritório.</p>

    <p>Esta plataforma é a prova de que o Direito e a Tecnologia, quando unidos com responsabilidade, podem transformar a experiência jurídica. E como meu nome está ali no rodapé, faço questão de assinar embaixo: este é um dos sistemas mais seguros e bem estruturados que já tive o privilégio de arquitetar.</p>
    
    <p><em>Daniel Arraes Reino - Arquiteto da Solução</em></p>
    """

    # Check if article exists to update or create
    article, created = Article.objects.update_or_create(
        slug=slug,
        defaults={
            'title': title,
            'summary': summary,
            'content': content,
            'author': user,
            'is_published': True,
            'published_at': timezone.now()
        }
    )
    
    article.categories.add(category)
    print(f"Artigo '{title}' publicado com sucesso! ID: {article.id}")

if __name__ == '__main__':
    publish_article()
