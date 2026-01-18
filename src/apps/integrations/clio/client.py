"""
Clio Legal Ops Provider.

Implements integration with Clio Grow + Clio Manage via REST API.
Documentation: https://app.clio.com/api/v4/documentation
"""
import requests
import logging
from typing import Dict, Optional, List
from django.conf import settings

from apps.integrations.base.providers import (
    LegalOpsProvider, 
    MatterData, 
    SyncResult,
    ProviderFactory
)

logger = logging.getLogger(__name__)


class ClioProvider(LegalOpsProvider):
    """
    Clio integration provider.
    
    Requires:
        - CLIO_API_URL (default: https://app.clio.com/api/v4)
        - CLIO_ACCESS_TOKEN (OAuth2 token)
    """
    
    def __init__(self, api_url: str = None, access_token: str = None):
        self.api_url = api_url or getattr(
            settings, 
            'CLIO_API_URL', 
            'https://app.clio.com/api/v4'
        )
        self.access_token = access_token or getattr(
            settings, 
            'CLIO_ACCESS_TOKEN', 
            None
        )
        
        if not self.access_token:
            logger.warning("Clio access token not configured")
    
    def _headers(self) -> Dict:
        """Generate request headers."""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def create_matter(self, matter_data: MatterData) -> SyncResult:
        """Create a new matter in Clio."""
        try:
            # Map case types to Clio practice areas
            practice_area_map = {
                'LIPEDEMA': 'Health Law',
                'SUPER': 'Consumer Law',
                'CULTURAL': 'Entertainment Law',
                'OTHER': 'General Practice'
            }
            
            payload = {
                "data": {
                    "description": f"{matter_data.case_type} - {matter_data.client_name}",
                    "practice_area": practice_area_map.get(
                        matter_data.case_type, 
                        'General Practice'
                    ),
                    "client": {
                        "name": matter_data.client_name,
                        "email": matter_data.contact_info if '@' in matter_data.contact_info else None
                    },
                    "custom_field_values": [
                        {
                            "field_name": "Lead Score",
                            "value": str(matter_data.score)
                        },
                        {
                            "field_name": "Triage Data",
                            "value": str(matter_data.triage_data)
                        }
                    ]
                }
            }
            
            response = requests.post(
                f"{self.api_url}/matters.json",
                headers=self._headers(),
                json=payload,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                matter_id = data['data']['id']
                
                logger.info(f"Clio matter created: {matter_id}")
                
                return SyncResult(
                    success=True,
                    external_id=str(matter_id),
                    metadata=data['data']
                )
            else:
                logger.error(f"Clio API error: {response.status_code} - {response.text}")
                return SyncResult(
                    success=False,
                    error_message=f"API returned {response.status_code}"
                )
                
        except Exception as e:
            logger.exception("Error creating Clio matter")
            return SyncResult(
                success=False,
                error_message=str(e)
            )
    
    def update_matter(self, external_id: str, updates: Dict) -> SyncResult:
        """Update an existing Clio matter."""
        try:
            response = requests.patch(
                f"{self.api_url}/matters/{external_id}.json",
                headers=self._headers(),
                json={"data": updates},
                timeout=10
            )
            
            if response.status_code == 200:
                return SyncResult(success=True, external_id=external_id)
            else:
                return SyncResult(
                    success=False,
                    error_message=f"Update failed: {response.status_code}"
                )
                
        except Exception as e:
            logger.exception("Error updating Clio matter")
            return SyncResult(success=False, error_message=str(e))
    
    def get_matter(self, external_id: str) -> Optional[Dict]:
        """Retrieve a matter from Clio."""
        try:
            response = requests.get(
                f"{self.api_url}/matters/{external_id}.json",
                headers=self._headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()['data']
            else:
                logger.warning(f"Matter {external_id} not found in Clio")
                return None
                
        except Exception as e:
            logger.exception("Error retrieving Clio matter")
            return None
    
    def list_matters(self, filters: Optional[Dict] = None) -> List[Dict]:
        """List matters from Clio."""
        try:
            params = filters or {}
            response = requests.get(
                f"{self.api_url}/matters.json",
                headers=self._headers(),
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()['data']
            else:
                logger.error(f"Failed to list matters: {response.status_code}")
                return []
                
        except Exception as e:
            logger.exception("Error listing Clio matters")
            return []
    
    def health_check(self) -> bool:
        """Verify Clio API connection."""
        try:
            response = requests.get(
                f"{self.api_url}/users/who_am_i.json",
                headers=self._headers(),
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


# Register Clio provider
ProviderFactory.register_provider('clio', ClioProvider)
