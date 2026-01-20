import os
import django

# Setup process
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User, Group
from apps.clients.models import Client
from apps.legal_cases.models import LegalCase
from apps.portals.models import ClientPortalAccess, CaseTimeline

def create_test_users():
    # 1. Create Groups if they don't exist
    for group_name in ['Manager', 'Secretary', 'Client']:
        Group.objects.get_or_create(name=group_name)
    
    # 2. Admin Full (Superuser)
    if not User.objects.filter(username='alessandra_admin').exists():
        User.objects.create_superuser('alessandra_admin', 'alessandra@japa.legal', 'alessandra123')
        print(">>> Superuser created: alessandra_admin / alessandra123 <<<")
    
    # 3. Manager
    if not User.objects.filter(username='alessandra_manager').exists():
        user = User.objects.create_user('alessandra_manager', 'manager@japa.legal', 'alessandra123')
        user.groups.add(Group.objects.get(name='Manager'))
        print(">>> Manager created: alessandra_manager / alessandra123 <<<")

    # 4. Secretary
    if not User.objects.filter(username='alessandra_secretary').exists():
        user = User.objects.create_user('alessandra_secretary', 'secretary@japa.legal', 'alessandra123')
        user.groups.add(Group.objects.get(name='Secretary'))
        print(">>> Secretary created: alessandra_secretary / alessandra123 <<<")

    # 5. Client
    if not User.objects.filter(username='alessandra_client').exists():
        user = User.objects.create_user('alessandra_client', 'client@japa.legal', 'alessandra123')
        user.groups.add(Group.objects.get(name='Client'))
        
        # Create associated Client record
        client_record, _ = Client.objects.get_or_create(
            full_name="Alessandra Cliente Teste",
            email="client@japa.legal",
            defaults={'cpf_cnpj': '12345678901', 'phone': '19993257342'}
        )
        
        # Create a sample case
        legal_case, _ = LegalCase.objects.get_or_create(
            client=client_record,
            title="Caso Exemplo - Alessandra",
            defaults={'area': 'HEALTH', 'status': 'ACTIVE'}
        )
        
        # Create Portal Access
        access, _ = ClientPortalAccess.objects.get_or_create(
            client=client_record,
            legal_case=legal_case,
            defaults={'access_token': 'alessandra-test-token-2026', 'is_active': True}
        )
        
        # Create Timeline
        timeline, _ = CaseTimeline.objects.get_or_create(
            legal_case=legal_case,
            defaults={'current_stage': 'ANALYSIS'}
        )
        timeline.add_milestone('INTAKE', 'Início da triagem', user)
        timeline.add_milestone('ANALYSIS', 'Caso em análise técnica', user)

        print(">>> Client created: alessandra_client / alessandra123 <<<")
        print(f">>> Portal Access Token: {access.access_token} <<<")

if __name__ == "__main__":
    create_test_users()
