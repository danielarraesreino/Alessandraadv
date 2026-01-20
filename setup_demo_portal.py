import os
import sys
import django
from django.utils import timezone

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from apps.clients.models import Client
from apps.legal_cases.models import LegalCase
from apps.portals.models import ClientPortalAccess

def setup_demo():
    # 1. Create Client
    client, _ = Client.objects.get_or_create(
        full_name="João Silva (Demo)",
        defaults={
            "phone": "+5511999998888",
            "email": "joao.demo@example.com",
            "cpf_cnpj": "123.456.789-00",
            "client_type": "PF",
            "status": "ACTIVE"
        }
    )
    print(f"Client: {client}")

    # 2. Create Case
    case, _ = LegalCase.objects.get_or_create(
        client=client,
        title="Ação Indenizatória Lipedema",
        defaults={
            "area": "CIVIL",
            "status": "ANALYSIS",
            "process_number": "1002345-88.2025.8.26.0114",
            "description": "Caso piloto para demonstração do portal.",
            "entry_date": timezone.now().date()
        }
    )
    print(f"Case: {case}")
    
    # 3. Create Timeline Mock Data (if empty)
    try:
        timeline = case.timeline
    except Exception:
        from apps.portals.models import CaseTimeline
        timeline, _ = CaseTimeline.objects.get_or_create(
            legal_case=case,
            defaults={
                "current_stage": "ANALYSIS",
                "milestones": [
                    {"stage": "INTAKE", "date": timezone.now().strftime('%Y-%m-%d'), "completed": True},
                    {"stage": "ANALYSIS", "date": None, "completed": False}
                ]
            }
        )
        print(f"Timeline: {timeline}")

    import uuid
    # 4. Create Access Token
    access, created = ClientPortalAccess.objects.get_or_create(
        client=client,
        legal_case=case,
        defaults={
            "access_token": str(uuid.uuid4()).replace('-', ''),
            "is_active": True
        }
    )
    
    url = f"http://127.0.0.1:8000/portal/timeline/?token={access.access_token}"
    print(f"\nDEMO_URL={url}")

if __name__ == "__main__":
    setup_demo()
