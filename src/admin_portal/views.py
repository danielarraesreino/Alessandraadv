from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta
from apps.intake.models import Lead
from apps.clients.models import Client
from apps.legal_cases.models import LegalCase
from .models import SystemSettings
from in_brief.models import Article, Category
from django.contrib import messages
from .forms import ArticleForm
import os

def is_manager(user):
    return user.is_superuser or user.groups.filter(name='Manager').exists()

@login_required
@user_passes_test(is_manager)
def dashboard(request):
    """Dashboard principal com métricas."""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Métricas de Leads
    leads_today = Lead.objects.filter(created_at__date=today).count()
    leads_week = Lead.objects.filter(created_at__date__gte=week_ago).count()
    leads_month = Lead.objects.filter(created_at__date__gte=month_ago).count()
    leads_qualified = Lead.objects.filter(is_qualified=True).count()
    
    # Casos por área
    cases_by_area = LegalCase.objects.values('area').annotate(count=Count('id'))
    
    # Casos ativos
    active_cases = LegalCase.objects.filter(status='ACTIVE').count()
    
    # Total de clientes
    total_clients = Client.objects.count()
    
    # Métricas Financeiras
    finance_total_pending = AccountPayable.objects.filter(status='PENDING').aggregate(Sum('amount'))['amount__sum'] or 0
    finance_receivable_pending = AccountReceivable.objects.filter(status='PENDING').aggregate(Sum('amount'))['amount__sum'] or 0
    finance_late_count = AccountPayable.objects.filter(status='PENDING', due_date__lt=today).count()
    
    # Contingência de Risco
    total_contingency = LegalCase.objects.aggregate(Sum('contingency_value'))['contingency_value__sum'] or 0
    
    # Métricas de Conteúdo (In Brief)
    total_articles = Article.objects.count()
    published_articles = Article.objects.filter(is_published=True).count()
    categories_count = Category.objects.count()
    
    context = {
        'leads_today': leads_today,
        'leads_week': leads_week,
        'leads_month': leads_month,
        'leads_qualified': leads_qualified,
        'cases_by_area': cases_by_area,
        'active_cases': active_cases,
        'total_clients': total_clients,
        'finance_total_pending': finance_total_pending,
        'finance_receivable_pending': finance_receivable_pending,
        'finance_late_count': finance_late_count,
        'total_contingency': total_contingency,
        'total_articles': total_articles,
        'published_articles': published_articles,
        'categories_count': categories_count,
        'leads_by_source': Lead.objects.values('source').annotate(count=Count('id')),
        'leads_by_location': Lead.objects.values('location').annotate(count=Count('id')),
    }
    
    return render(request, 'admin_portal/dashboard.html', context)

@login_required
def leads_kanban(request):
    """Kanban board de leads."""
    # Organizar leads por status (simulado com is_qualified)
    new_leads = Lead.objects.filter(is_qualified=False, external_id__isnull=True).order_by('-created_at')
    qualified_leads = Lead.objects.filter(is_qualified=True, external_id__isnull=True).order_by('-created_at')
    converted_leads = Lead.objects.filter(external_id__isnull=False).order_by('-created_at')
    
    context = {
        'new_leads': new_leads,
        'qualified_leads': qualified_leads,
        'converted_leads': converted_leads,
    }
    
    return render(request, 'admin_portal/leads_kanban.html', context)

@login_required
def lead_detail(request, lead_id):
    """Detalhes de um lead específico com cálculo de score se for 0."""
    lead = get_object_or_404(Lead, id=lead_id)
    
    # Simulação de cálculo de score se ainda estiver zerado
    if lead.score == 0:
        score = 50  # Base
        if lead.case_type in ['LIPEDEMA', 'HEALTH']: score += 20
        if lead.case_type == 'SUPER': score += 15
        if lead.location and 'Campinas' in lead.location: score += 10
        
        lead.score = min(score, 100)
        lead.save()

    context = {
        'lead': lead,
    }
    
    return render(request, 'admin_portal/lead_detail.html', context)

@login_required
def convert_lead(request, lead_id):
    """Converter lead em cliente."""
    lead = get_object_or_404(Lead, id=lead_id)
    
    if request.method == 'POST':
        # Criar cliente a partir do lead
        client = Client.objects.create(
            full_name=lead.full_name,
            client_type='PF',  # Padrão
            cpf_cnpj='000.000.000-00',  # Placeholder - usuário deve editar depois
            phone=lead.contact_info,
            email=lead.contact_info if '@' in lead.contact_info else '',
        )
        
        # Marcar lead como convertido
        lead.external_id = f'CLIENT_{client.id}'
        lead.save()
        
        return redirect('admin_portal:client_detail', client_id=client.id)
    
    return redirect('admin_portal:lead_detail', lead_id=lead_id)

# ============ CLIENTS VIEWS ============

@login_required
def clients_list(request):
    """Lista de clientes com busca."""
    search_query = request.GET.get('search', '')
    client_type = request.GET.get('type', '')
    
    clients = Client.objects.all()
    
    # Busca por nome, email
    if search_query:
        clients = clients.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Filtro por tipo
    if client_type:
        clients = clients.filter(client_type=client_type)
    
    # Kanban Logic
    prospects = clients.filter(status='PROSPECT').order_by('-created_at')
    onboarding = clients.filter(status='ONBOARDING').order_by('-created_at')
    active = clients.filter(status='ACTIVE').order_by('-created_at')
    archived = clients.filter(status='ARCHIVED').order_by('-created_at')
    
    context = {
        'prospects': prospects,
        'onboarding': onboarding,
        'active': active,
        'archived': archived,
        'search_query': search_query,
    }
    
    return render(request, 'admin_portal/clients_kanban.html', context)

@login_required
def client_detail(request, client_id):
    """Perfil completo do cliente."""
    client = get_object_or_404(Client, id=client_id)
    cases = client.cases.all().order_by('-entry_date')
    
    context = {
        'client': client,
        'cases': cases,
    }
    
    return render(request, 'admin_portal/client_detail.html', context)

@login_required
def client_create(request):
    """Criar novo cliente."""
    if request.method == 'POST':
        client = Client.objects.create(
            full_name=request.POST.get('full_name'),
            client_type=request.POST.get('client_type', 'PF'),
            cpf_cnpj=request.POST.get('cpf_cnpj'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email', ''),
        )
        return redirect('admin_portal:client_detail', client_id=client.id)
    
    return render(request, 'admin_portal/client_form.html', {'client': None})

@login_required
def client_edit(request, client_id):
    """Editar cliente existente."""
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == 'POST':
        client.full_name = request.POST.get('full_name')
        client.client_type = request.POST.get('client_type')
        client.cpf_cnpj = request.POST.get('cpf_cnpj')
        client.phone = request.POST.get('phone')
        client.email = request.POST.get('email', '')
        client.save()
        return redirect('admin_portal:client_detail', client_id=client.id)
    
    return render(request, 'admin_portal/client_form.html', {'client': client})

# ============ CASES VIEWS ============

@login_required
def cases_kanban(request):
    """Kanban board de casos por status."""
    analysis_cases = LegalCase.objects.filter(status='ANALYSIS').order_by('-entry_date')
    active_cases = LegalCase.objects.filter(status='ACTIVE').order_by('-entry_date')
    suspended_cases = LegalCase.objects.filter(status='SUSPENDED').order_by('-entry_date')
    archived_cases = LegalCase.objects.filter(status='ARCHIVED').order_by('-entry_date')
    
    context = {
        'analysis_cases': analysis_cases,
        'active_cases': active_cases,
        'suspended_cases': suspended_cases,
        'archived_cases': archived_cases,
    }
    
    return render(request, 'admin_portal/cases_kanban.html', context)

@login_required
def case_detail(request, case_id):
    """Detalhes do caso com timeline."""
    case = get_object_or_404(LegalCase, id=case_id)
    
    # Tentar pegar timeline se existir
    timeline = None
    if hasattr(case, 'timeline'):
        timeline = case.timeline
    
    context = {
        'case': case,
        'timeline': timeline,
    }
    
    return render(request, 'admin_portal/case_detail.html', context)

@login_required
def case_create(request):
    """Criar novo caso."""
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        client = get_object_or_404(Client, id=client_id)
        
        case = LegalCase.objects.create(
            client=client,
            title=request.POST.get('title'),
            area=request.POST.get('area'),
            status=request.POST.get('status', 'ANALYSIS'),
            process_number=request.POST.get('process_number', ''),
            description=request.POST.get('description', ''),
        )
        return redirect('admin_portal:case_detail', case_id=case.id)
    
    # Lista de clientes para o formulário
    clients = Client.objects.all().order_by('full_name')
    
    return render(request, 'admin_portal/case_form.html', {'case': None, 'clients': clients})

@login_required
def case_edit(request, case_id):
    """Editar caso existente."""
    case = get_object_or_404(LegalCase, id=case_id)
    
    if request.method == 'POST':
        case.title = request.POST.get('title')
        case.area = request.POST.get('area')
        case.status = request.POST.get('status')
        case.process_number = request.POST.get('process_number', '')
        case.description = request.POST.get('description', '')
        case.save()
        return redirect('admin_portal:case_detail', case_id=case.id)
    
    clients = Client.objects.all().order_by('full_name')
    
    return render(request, 'admin_portal/case_form.html', {'case': case, 'clients': clients})

from apps.finance.models import AccountPayable, AccountReceivable

@login_required
@user_passes_test(is_manager)
def finance_list(request):
    """Lista de finanças (Pagar/Receber) com filtros."""
    tab = request.GET.get('tab', 'payable')
    status_filter = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')
    
    if tab == 'receivable':
        items = AccountReceivable.objects.all()
        status_choices = AccountReceivable.STATUS_CHOICES
        category_choices = AccountReceivable.CATEGORY_CHOICES
    else:
        items = AccountPayable.objects.all()
        status_choices = AccountPayable.STATUS_CHOICES
        category_choices = AccountPayable.CATEGORY_CHOICES
    
    if status_filter:
        items = items.filter(status=status_filter)
    if category_filter:
        items = items.filter(category=category_filter)
        
    items = items.order_by('due_date')
    
    context = {
        'items': items,
        'tab': tab,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'STATUS_CHOICES': status_choices,
        'CATEGORY_CHOICES': category_choices,
    }
    
    return render(request, 'admin_portal/finance_list.html', context)

@login_required
def finance_create(request):
    """Criar nova conta a pagar."""
    if request.method == 'POST':
        item = AccountPayable.objects.create(
            description=request.POST.get('description'),
            supplier=request.POST.get('supplier', ''),
            amount=request.POST.get('amount'),
            due_date=request.POST.get('due_date'),
            category=request.POST.get('category', 'OTHER'),
            status='PENDING',
            notes=request.POST.get('notes', ''),
        )
        return redirect('admin_portal:finance_list')
    
    context = {
        'CATEGORY_CHOICES': AccountPayable.CATEGORY_CHOICES,
    }
    
    return render(request, 'admin_portal/finance_form.html', context)

@login_required
def finance_pay(request, item_id):
    """Marcar conta como paga ou recebida (suporta HTMX)."""
    tab = request.GET.get('tab', 'payable')
    
    if tab == 'receivable':
        item = get_object_or_404(AccountReceivable, id=item_id)
        item.status = 'RECEIVED'
        item.received_date = timezone.now().date()
        item.save()
        label = 'Recebido'
    else:
        item = get_object_or_404(AccountPayable, id=item_id)
        item.status = 'PAID'
        item.save()
        label = 'Pago'
    
    if request.headers.get('HX-Request'):
        return HttpResponse(f'<span class="badge badge-success" style="background: #dcfce7; color: #166534; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem;">{label}</span>')
    
    return redirect(f"{reverse('admin_portal:finance_list')}?tab={tab}")

# ============ SETTINGS VIEWS ============

@login_required
@user_passes_test(is_manager)
def settings_general(request):
    """Painel de configurações e integrações."""
    settings = SystemSettings.get_settings()
    
    if request.method == 'POST':
        settings.whatsapp_enabled = request.POST.get('whatsapp_enabled') == 'on'
        settings.clio_integration_active = request.POST.get('clio_integration_active') == 'on'
        settings.jestor_integration_active = request.POST.get('jestor_integration_active') == 'on'
        settings.client_notification_auto = request.POST.get('client_notification_auto') == 'on'
        settings.token_validity_days = int(request.POST.get('token_validity_days', 30))
        settings.office_name = request.POST.get('office_name', settings.office_name)
        settings.save()
        messages.success(request, "Configurações atualizadas com sucesso!")
        return redirect('admin_portal:settings_general')

    context = {
        'settings': settings,
        'integrations': [
            {'name': 'WhatsApp (WPPConnect)', 'status': 'CONECTADO' if settings.whatsapp_enabled else 'DESCONECTADO', 'type': 'SISTEMA', 'enabled': settings.whatsapp_enabled},
            {'name': 'Clio (Legal Ops)', 'status': 'CONECTADO' if settings.clio_integration_active else 'PENDENTE', 'type': 'MOCK', 'enabled': settings.clio_integration_active},
            {'name': 'Jestor (Database)', 'status': 'CONECTADO' if settings.jestor_integration_active else 'PENDENTE', 'type': 'MOCK', 'enabled': settings.jestor_integration_active},
        ]
    }
    return render(request, 'admin_portal/settings_general.html', context)

from apps.legal_cases.services.document_service import DocumentAutomationService
from django.http import FileResponse

@login_required
def generate_document_action(request, case_id):
    """Gera um documento .docx para o caso."""
    case = get_object_or_404(LegalCase, id=case_id)
    service = DocumentAutomationService()
    
    try:
        output_path = service.generate_base_document(case)
        return FileResponse(
            open(output_path, 'rb'), 
            as_attachment=True, 
            filename=os.path.basename(output_path)
        )
    except Exception as e:
        messages.error(request, f"Erro ao gerar documento: {e}")
        return redirect('admin_portal:case_detail', case_id=case_id)

# ============ ARTICLES VIEWS ============

@login_required
def article_list(request):
    """Lista de artigos do In Brief com métricas rápidas."""
    articles = Article.objects.all().order_by('-created_at')
    
    # Métricas para o topo da página
    total_count = articles.count()
    published_count = articles.filter(is_published=True).count()
    draft_count = total_count - published_count
    
    context = {
        'articles': articles,
        'total_count': total_count,
        'published_count': published_count,
        'draft_count': draft_count,
    }
    return render(request, 'admin_portal/article_list.html', context)

@login_required
def article_create(request):
    """Criar novo artigo usando ArticleForm."""
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            from django.utils.text import slugify
            article.slug = slugify(article.title)
            if article.is_published:
                article.published_at = timezone.now()
            article.save()
            form.save_m2m() # Save categories
            messages.success(request, "Artigo criado com sucesso!")
            return redirect('admin_portal:article_list')
    else:
        form = ArticleForm()
    
    return render(request, 'admin_portal/article_form.html', {'form': form, 'article': None})

@login_required
def article_edit(request, article_id):
    """Editar artigo existente usando ArticleForm."""
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            was_published = article.is_published
            article = form.save(commit=False)
            if article.is_published and not was_published:
                article.published_at = timezone.now()
            article.save()
            form.save_m2m()
            messages.success(request, "Artigo atualizado com sucesso!")
            return redirect('admin_portal:article_list')
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'admin_portal/article_form.html', {'form': form, 'article': article})

@login_required
def article_delete(request, article_id):
    """Excluir artigo."""
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        messages.success(request, "Artigo excluído com sucesso!")
        return redirect('admin_portal:article_list')
    return render(request, 'admin_portal/article_confirm_delete.html', {'article': article})

# ============ CATEGORIES VIEWS ============

@login_required
def category_list(request):
    """Lista de categorias do In Brief."""
    categories = Category.objects.annotate(article_count=Count('articles'))
    return render(request, 'admin_portal/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    """Criar nova categoria."""
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name, slug=slugify(name))
        messages.success(request, "Categoria criada com sucesso!")
        return redirect('admin_portal:category_list')
    return render(request, 'admin_portal/category_form.html', {'category': None})

@login_required
def category_edit(request, category_id):
    """Editar categoria existente."""
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.slug = slugify(category.name)
        category.save()
        messages.success(request, "Categoria atualizada com sucesso!")
        return redirect('admin_portal:category_list')
    return render(request, 'admin_portal/category_form.html', {'category': category})

@login_required
def category_delete(request, category_id):
    """Excluir categoria."""
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Categoria excluída com sucesso!")
        return redirect('admin_portal:category_list')
    return render(request, 'admin_portal/category_confirm_delete.html', {'category': category})
