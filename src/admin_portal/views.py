from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from apps.intake.models import Lead
from apps.clients.models import Client
from apps.legal_cases.models import LegalCase

@login_required
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
    
    context = {
        'leads_today': leads_today,
        'leads_week': leads_week,
        'leads_month': leads_month,
        'leads_qualified': leads_qualified,
        'cases_by_area': cases_by_area,
        'active_cases': active_cases,
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
    """Detalhes de um lead específico."""
    lead = get_object_or_404(Lead, id=lead_id)
    
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
        
        return redirect('admin_portal:leads_kanban')
    
    return redirect('admin_portal:lead_detail', lead_id=lead_id)
