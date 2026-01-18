"""
Tests for Legal Ops integrations.
"""
import pytest
from unittest.mock import Mock, patch
from django.test import TestCase

from apps.intake.models import Lead
from apps.integrations.base.providers import MatterData, SyncResult
from apps.integrations.base.sync_service import LegalOpsSyncService
from apps.integrations.clio.client import ClioProvider


class ClioProviderTestCase(TestCase):
    """Tests for Clio provider."""
    
    def setUp(self):
        self.provider = ClioProvider(
            api_url='https://test.clio.com/api/v4',
            access_token='test_token'
        )
    
    @patch('apps.integrations.clio.client.requests.post')
    def test_create_matter_success(self, mock_post):
        """Test successful matter creation in Clio."""
        # Mock API response
        mock_post.return_value = Mock(
            status_code=201,
            json=lambda: {
                'data': {
                    'id': 12345,
                    'description': 'Test Matter'
                }
            }
        )
        
        matter_data = MatterData(
            client_name="Test Client",
            case_type="LIPEDEMA",
            description="Test case",
            contact_info="test@example.com",
            score=85,
            triage_data={'test': 'data'}
        )
        
        result = self.provider.create_matter(matter_data)
        
        self.assertTrue(result.success)
        self.assertEqual(result.external_id, '12345')
        mock_post.assert_called_once()
    
    @patch('apps.integrations.clio.client.requests.post')
    def test_create_matter_failure(self, mock_post):
        """Test failed matter creation."""
        mock_post.return_value = Mock(
            status_code=400,
            text='Bad Request'
        )
        
        matter_data = MatterData(
            client_name="Test Client",
            case_type="LIPEDEMA",
            description="Test case",
            contact_info="test@example.com",
            score=85,
            triage_data={}
        )
        
        result = self.provider.create_matter(matter_data)
        
        self.assertFalse(result.success)
        self.assertIn('400', result.error_message)


class SyncServiceTestCase(TestCase):
    """Tests for sync service."""
    
    def setUp(self):
        self.lead = Lead.objects.create(
            full_name="Integration Test Lead",
            case_type="LIPEDEMA",
            contact_info="(19) 99999-8888",
            score=75,
            is_qualified=True,
            triage_data={'negativa': 'sim'}
        )
    
    @patch('apps.integrations.base.sync_service.ProviderFactory.get_provider')
    def test_sync_qualified_lead(self, mock_get_provider):
        """Test syncing a qualified lead."""
        # Mock provider
        mock_provider = Mock()
        mock_provider.create_matter.return_value = SyncResult(
            success=True,
            external_id='clio-12345'
        )
        mock_get_provider.return_value = mock_provider
        
        sync_service = LegalOpsSyncService(provider_name='clio')
        result = sync_service.sync_lead_to_matter(self.lead)
        
        self.assertTrue(result.success)
        self.assertEqual(result.external_id, 'clio-12345')
        
        # Verify lead was updated
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.external_id, 'clio-12345')
    
    def test_sync_unqualified_lead(self):
        """Test that unqualified leads are not synced."""
        unqualified_lead = Lead.objects.create(
            full_name="Unqualified Lead",
            case_type="OTHER",
            contact_info="test@example.com",
            score=30,
            is_qualified=False
        )
        
        sync_service = LegalOpsSyncService()
        result = sync_service.sync_lead_to_matter(unqualified_lead)
        
        self.assertFalse(result.success)
        self.assertIn('not qualified', result.error_message)
    
    @patch('apps.integrations.base.sync_service.ProviderFactory.get_provider')
    def test_already_synced_lead(self, mock_get_provider):
        """Test that already synced leads are skipped."""
        self.lead.external_id = 'existing-id'
        self.lead.save()
        
        sync_service = LegalOpsSyncService()
        result = sync_service.sync_lead_to_matter(self.lead)
        
        self.assertTrue(result.success)
        self.assertEqual(result.external_id, 'existing-id')
        # Provider should not be called
        mock_get_provider.return_value.create_matter.assert_not_called()


@pytest.mark.django_db
class TestIntegrationAPI:
    """Tests for integration API endpoints."""
    
    def test_sync_endpoint_with_qualified_lead(self, client):
        """Test /api/integrations/sync/lead-to-matter/ endpoint."""
        lead = Lead.objects.create(
            full_name="API Test Lead",
            case_type="SUPER",
            contact_info="(11) 98765-4321",
            score=80,
            is_qualified=True
        )
        
        with patch('apps.integrations.base.sync_service.ProviderFactory.get_provider') as mock:
            mock_provider = Mock()
            mock_provider.create_matter.return_value = SyncResult(
                success=True,
                external_id='api-test-123'
            )
            mock.return_value = mock_provider
            
            response = client.post(f'/api/integrations/sync/lead-to-matter/{lead.id}/')
            
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is True
            assert data['external_id'] == 'api-test-123'
