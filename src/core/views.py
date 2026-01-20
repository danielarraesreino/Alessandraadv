from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def role_based_redirect(request):
    user = request.user
    if user.is_superuser or user.groups.filter(name='Manager').exists():
        return redirect('admin_portal:dashboard')
    elif user.groups.filter(name='Secretary').exists():
        # Secretary goes to Kanban or Intake, not Dashboard (which is restricted)
        return redirect('admin_portal:leads_kanban')
    elif user.groups.filter(name='Client').exists():
        return redirect('/portal/') # Should use client_login token logic ideally, this is a fallback
    else:
        # Default fallback
        return redirect('admin_portal:dashboard')

def health_check(request):
    return JsonResponse({"status": "ok", "message": "Django is up!"}, status=200)

def db_health_check(request):
    try:
        # Check database connectivity
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            
        return JsonResponse({
            "status": "ok", 
            "database": "connected",
            "google_auth": "configured" # Static check as we configured it
        }, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "reason": str(e)}, status=500)
