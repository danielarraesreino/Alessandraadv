from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connection
from django.contrib.auth.decorators import login_required

def privacy_policy(request):
    """LGPD Privacy Policy page."""
    return render(request, 'privacy_policy.html')

@login_required
def role_based_redirect(request):
    user = request.user
    if user.is_superuser or user.groups.filter(name='Manager').exists():
        return redirect('admin_portal:dashboard')
    elif user.groups.filter(name='Secretary').exists():
        return redirect('admin_portal:leads_kanban')
    elif user.groups.filter(name='Client').exists():
        return redirect('/portal/')
    else:
        return redirect('admin_portal:dashboard')

def health_check(request):
    """Simple health check endpoint."""
    return JsonResponse({"status": "ok", "message": "Legal Intelligence Platform is online"}, status=200)
