from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.core.management import call_command
from apps.clients.models import Client
from apps.legal_cases.models import LegalCase
from apps.portals.models import ClientPortalAccess, CaseTimeline

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

        # 4. Setup Client (Database Only, Portal is Token-Based)
        client_record, _ = Client.objects.get_or_create(
            email='cliente@demo.com',
            defaults={
                'full_name': 'Cliente Demonstração',
                'status': 'ACTIVE',
                'cpf_cnpj': '000.000.000-00',
                'phone': '(19) 99325-7342'
            }
        )
        
        # Create a dummy cases
        cases_data = [
            {
                'title': 'Processo de Demonstração - Fase 4',
                'process_number': '12345.678/2026',
                'status': 'ACTIVE',
                'area': 'CIVIL',
                'description': 'Acesso demonstrativo para validação da UI da Fase 4.'
            },
            {
                'title': 'Recurso Ordinário - Lipedema',
                'process_number': '5001234-55.2026.4.03.6100',
                'status': 'ANALYSIS',
                'area': 'SAUDE',
                'description': 'Acompanhamento de recurso para cirurgia reparadora.'
            },
            {
                'title': 'Habilitação de Crédito - Superendividamento',
                'process_number': '0008765-12.2025.8.26.0100',
                'status': 'FILED',
                'area': 'CONSUMIDOR',
                'description': 'Repactuação de dívidas sob a égide da Lei 14.181.'
            }
        ]

        from django.core.files.base import ContentFile
        from apps.portals.models import CaseDocument

        for case_info in cases_data:
            legal_case, _ = LegalCase.objects.get_or_create(
                client=client_record,
                title=case_info['title'],
                defaults={
                    'process_number': case_info['process_number'],
                    'status': case_info['status'],
                    'area': case_info['area'],
                    'description': case_info['description']
                }
            )
            
            # Ensure CaseTimeline exists
            CaseTimeline.objects.get_or_create(legal_case=legal_case)

            # Add a mock document
            CaseDocument.objects.get_or_create(
                legal_case=legal_case,
                title=f"Documento de {case_info['title']}",
                defaults={
                    'document_type': 'OTHER',
                    'description': 'Arquivo de demonstração gerado automaticamente.',
                    'file': ContentFile(b'Demo content', name=f'demo_{legal_case.id}.pdf'),
                    'is_visible_to_client': True
                }
            )
        
        # Create Portal Access with static token
        ClientPortalAccess.objects.get_or_create(
            client=client_record,
            legal_case=LegalCase.objects.filter(client=client_record).first(),
            defaults={
                'access_token': 'demo-token-2026',
                'is_active': True
            }
        )

        self.stdout.write(self.style.SUCCESS(f'Client demo setup complete. Token: demo-token-2026'))
