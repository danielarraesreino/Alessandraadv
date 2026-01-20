from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.intake.models import Lead
from apps.legal_cases.models import LegalCase

class Command(BaseCommand):
    help = 'Setup initial user roles and permissions'

    def handle(self, *args, **options):
        # 1. Manager (Gestor)
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        # Manager gets all permissions (effectively superuser for business logic)
        # For now, we assume they are Superusers or have granular permissions added manually if needed.
        # But commonly, we give them all model permissions.
        self.stdout.write(self.style.SUCCESS('Manager group created'))

        # 2. Secretary (Secretaria/Paralegal)
        secretary_group, _ = Group.objects.get_or_create(name='Secretary')
        
        # Permissions for Secretary
        # Can View/Add/Change Leads (Intake)
        lead_ct = ContentType.objects.get_for_model(Lead)
        sec_perms = Permission.objects.filter(
            content_type=lead_ct, 
            codename__in=['view_lead', 'add_lead', 'change_lead']
        )
        secretary_group.permissions.set(sec_perms)
        
        # Can View Legal Cases (but not delete or sensitive fields if we had them separated)
        case_ct = ContentType.objects.get_for_model(LegalCase)
        case_perms = Permission.objects.filter(
            content_type=case_ct,
            codename__in=['view_legalcase']
        )
        secretary_group.permissions.add(*case_perms)
        
        self.stdout.write(self.style.SUCCESS('Secretary group created with restricted permissions'))

        # 3. Client (Cliente)
        client_group, _ = Group.objects.get_or_create(name='Client')
        # Clients usually have NO generic permissions, they only access object-level data via Portal views
        # which check for ownership (request.user == case.client.user).
        # So we leave permissions empty to be safe.
        client_group.permissions.clear()
        
        self.stdout.write(self.style.SUCCESS('Client group created (No generic permissions)'))
