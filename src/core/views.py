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
