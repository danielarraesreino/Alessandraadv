from typing import Dict, Optional, List
from ..base.providers import LegalOpsProvider, MatterData, SyncResult
from apps.legal_cases.models import LegalCase
from apps.clients.models import Client

class NativeProvider(LegalOpsProvider):
    """
    Native Django ORM implementation of LegalOpsProvider.
    """
    def create_matter(self, matter_data: MatterData) -> SyncResult:
        try:
            client, _ = Client.objects.get_or_create(
                full_name=matter_data.client_name,
                defaults={'phone': matter_data.contact_info}
            )
            
            # Map case_type to AREA_CHOICES if possible, else OTHER
            area_map = {
                'CIVIL': 'CIVIL',
                'BUSINESS': 'BUSINESS',
                'HEALTH': 'HEALTH',
                'THIRD_SECTOR': 'THIRD_SECTOR'
            }
            area = area_map.get(matter_data.case_type, 'OTHER')

            case = LegalCase.objects.create(
                client=client,
                title=f"Caso: {matter_data.case_type}",
                description=matter_data.description,
                area=area,
                status='ANALYSIS'
            )
            return SyncResult(success=True, external_id=str(case.id))
        except Exception as e:
            return SyncResult(success=False, error_message=str(e))

    def update_matter(self, external_id: str, updates: Dict) -> SyncResult:
        try:
            LegalCase.objects.filter(id=external_id).update(**updates)
            return SyncResult(success=True, external_id=external_id)
        except Exception as e:
            return SyncResult(success=False, error_message=str(e))

    def get_matter(self, external_id: str) -> Optional[Dict]:
        try:
            case = LegalCase.objects.get(id=external_id)
            return {
                'id': str(case.id),
                'title': case.title,
                'status': case.status
            }
        except LegalCase.DoesNotExist:
            return None

    def list_matters(self, filters: Optional[Dict] = None) -> List[Dict]:
        qs = LegalCase.objects.all()
        if filters:
            qs = qs.filter(**filters)
        return [{'id': str(c.id), 'title': c.title} for c in qs]

    def health_check(self) -> bool:
        return True
