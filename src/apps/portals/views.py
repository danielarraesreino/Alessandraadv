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
            
    return render(request, 'portals/login.html')


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
    
    context = {
        'access': access,
        'client': access.client,
        'legal_case': access.legal_case,
        'timeline': access.legal_case.timeline if hasattr(access.legal_case, 'timeline') else None,
    }
    
    return render(request, 'portals/case_timeline.html', context)
