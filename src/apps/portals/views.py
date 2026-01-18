"""
Views for Client Portal.
"""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from apps.portals.models import ClientPortalAccess


def portal_timeline(request):
    """
    Render the case timeline portal.
    
    Expects 'token' query parameter.
    """
    access_token = request.GET.get('token')
    
    if not access_token:
        return HttpResponse("Token de acesso não fornecido", status=400)
    
    # Validate token exists (actual validation happens in API)
    try:
        access = ClientPortalAccess.objects.get(
            access_token=access_token,
            is_active=True
        )
    except ClientPortalAccess.DoesNotExist:
        return HttpResponse("Token inválido ou expirado", status=401)
    
    return render(request, 'portals/case_timeline.html')
