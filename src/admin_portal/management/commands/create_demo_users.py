from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.core.management import call_command
from apps.clients.models import Client
from apps.legal_cases.models import LegalCase
import uuid

class Command(BaseCommand):
    help = 'Create demo users for the platform presentation'

    def handle(self, *args, **options):
        # 1. Ensure roles exist
        call_command('setup_roles')
        
        manager_group = Group.objects.get(name='Manager')
        secretary_group = Group.objects.get(name='Secretary')
        client_group = Group.objects.get(name='Client')

        # 2. Setup Manager (Superuser)
        manager_user, created = User.objects.get_or_create(
            username='gestor_demo',
            defaults={
                'email': 'gestor@demo.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        manager_user.set_password('Donadon@2026')
        manager_user.groups.add(manager_group)
        manager_user.save()
        self.stdout.write(self.style.SUCCESS(f'Manager user created: gestor_demo / Donadon@2026'))

        # 3. Setup Secretary
        secretary_user, created = User.objects.get_or_create(
            username='secretaria_demo',
            defaults={
                'email': 'secretaria@demo.com',
                'is_staff': True
            }
        )
        secretary_user.set_password('Donadon@2026')
        secretary_user.groups.add(secretary_group)
        secretary_user.save()
        self.stdout.write(self.style.SUCCESS(f'Secretary user created: secretaria_demo / Donadon@2026'))

        # 4. Setup Client
        client_user, created = User.objects.get_or_create(
            username='cliente_demo',
            defaults={
                'email': 'cliente@demo.com'
            }
        )
        client_user.set_password('Donadon@2026')
        client_user.groups.add(client_group)
        client_user.save()
        
        # Ensure the Client model exists for this user
        client_record, _ = Client.objects.get_or_create(
            user=client_user,
            defaults={
                'full_name': 'Cliente Demonstração',
                'email': 'cliente@demo.com',
                'status': 'ACTIVE'
            }
        )
        
        # Create a dummy case for the client to see in the portal
        LegalCase.objects.get_or_create(
            client=client_record,
            title='Processo de Demonstração - Fase 4',
            defaults={
                'case_number': '12345.678/2026',
                'status': 'ACTIVE'
            }
        )

        self.stdout.write(self.style.SUCCESS(f'Client user created: cliente_demo / Donadon@2026'))
