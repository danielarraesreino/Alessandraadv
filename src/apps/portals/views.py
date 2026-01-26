"""
Views for Client Portal.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from apps.portals.models import ClientPortalAccess


def client_login(request):
    """
    Login page for clients using their access token.
    """
    if request.method == 'POST':
        token = request.POST.get('access_token')
        if not token:
            messages.error(request, "Por favor, informe seu token de acesso.")
            return render(request, 'portals/login.html')
            
        try:
            access = ClientPortalAccess.objects.get(
                access_token=token,
                is_active=True
            )
            # Record access
            access.record_access()
            # Redirect to timeline with token in URL
            return redirect(f"/portal/timeline/?token={token}")
        except ClientPortalAccess.DoesNotExist:
            messages.error(request, "Token inválido ou expirado. Entre em contato com o escritório.")
            
            
    # Fetch latest articles for the sidebar
    from in_brief.models import Article
    latest_articles = Article.objects.filter(is_published=True).order_by('-published_at')[:3]
    return render(request, 'portals/login.html', {'latest_articles': latest_articles})


def portal_timeline(request):
    """
    Render the case timeline portal.
    
    Expects 'token' query parameter.
    """
    access_token = request.GET.get('token')
    
    if not access_token:
        return redirect('client_login')
    
    # Validate token exists
    try:
        access = ClientPortalAccess.objects.get(
            access_token=access_token,
            is_active=True
        )
    except ClientPortalAccess.DoesNotExist:
        messages.error(request, "Sua sessão expirou ou o token é inválido.")
        return redirect('client_login')
    
    # Onboarding logic (Mission 3)
    show_onboarding = False
    onboarding_key = f"onboarding_shown_{access.access_token}"
    if not request.session.get(onboarding_key):
        show_onboarding = True
        request.session[onboarding_key] = True
        
    context = {
        'access': access,
        'client': access.client,
        'legal_case': access.legal_case,
        'timeline': access.legal_case.timeline if hasattr(access.legal_case, 'timeline') else None,
        'show_onboarding': show_onboarding,
        'progress_override': 55 if access.access_token == 'demo-token-2026' else None,
    }
    
    return render(request, 'portals/case_timeline.html', context)

def timeline_fragment(request, token):
    """Retorna o fragmento HTML da timeline para HTMX."""
    access = get_object_or_404(ClientPortalAccess, access_token=token, is_active=True)
    legal_case = access.legal_case
    timeline = legal_case.timeline if hasattr(legal_case, 'timeline') else None
    
    # Human-centric labels (centralizados no backend agora)
    STAGE_DETAILS = {
        'INTAKE': {'label': 'Acolhimento & Triagem', 'icon': 'heart', 'desc': 'Analisando documentos iniciais.'},
        'ANALYSIS': {'label': 'Análise Jurídica', 'icon': 'search', 'desc': 'Construindo fundamentação estratégica.'},
        'PETITION': {'label': 'Petição Elaborada', 'icon': 'pen-tool', 'desc': 'Sua petição está sendo redigida.'},
        'FILED': {'label': 'Protocolo Realizado', 'icon': 'file-check', 'desc': 'Processo distribuído no tribunal.'},
        'DISCOVERY': {'label': 'Instrução', 'icon': 'layers', 'desc': 'Fase de coleta de provas e depoimentos.'},
        'HEARING': {'label': 'Audiência', 'icon': 'users', 'desc': 'Encontro marcado com o magistrado.'},
        'DECISION': {'label': 'Sentença', 'icon': 'gavel', 'desc': 'O juiz proferiu sua decisão.'},
        'APPEAL': {'label': 'Recurso', 'icon': 'trending-up', 'desc': 'Questionando a decisão em instâncias superiores.'},
        'CLOSED': {'label': 'Concluído', 'icon': 'check-circle', 'desc': 'Caso encerrado com sucesso.'},
    }

    stages_data = []
    STAGES_LIST = [s[0] for s in timeline.STAGES] if timeline else []
    
    milestones = timeline.milestones if timeline else []
    
    for stage_code in STAGES_LIST:
        milestone = next((m for m in milestones if m['stage'] == stage_code), None)
        is_completed = milestone is not None
        is_active = timeline.current_stage == stage_code if timeline else False
        details = STAGE_DETAILS.get(stage_code, {'label': stage_code, 'icon': 'help-circle', 'desc': ''})
        
        stages_data.append({
            'code': stage_code,
            'label': details['label'],
            'icon': details['icon'],
            'desc': details['desc'],
            'is_completed': is_completed,
            'is_active': is_active,
            'date': milestone['date'] if is_completed else None
        })

    return render(request, 'portals/fragments/timeline_items.html', {'stages': stages_data})

def documents_fragment(request, token):
    """Retorna o fragmento HTML da lista de documentos para HTMX."""
    access = get_object_or_404(ClientPortalAccess, access_token=token, is_active=True)
    documents = access.legal_case.documents.filter(is_visible_to_client=True)
    return render(request, 'portals/fragments/document_list.html', {'documents': documents})
