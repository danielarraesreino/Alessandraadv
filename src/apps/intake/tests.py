"""
Testes para o sistema de Intake e notificação WhatsApp.
"""
import pytest
from django.test import TestCase
from apps.intake.models import Lead, TriageSession
from apps.whatsapp.services.notification import WhatsAppNotificationService


class LeadCreationTestCase(TestCase):
    """Testes de criação de leads."""
    
    def test_create_lead_with_high_score(self):
        """Testa criação de lead com score alto (qualificado)."""
        lead = Lead.objects.create(
            full_name="Maria Silva",
            case_type="LIPEDEMA",
            contact_info="(19) 98888-7777",
            score=75,
            is_qualified=True,
            triage_data={
                'negativa': 'sim',
                'urgencia': 'urgente'
            }
        )
        
        self.assertEqual(lead.full_name, "Maria Silva")
        self.assertEqual(lead.case_type, "LIPEDEMA")
        self.assertTrue(lead.is_qualified)
        self.assertGreater(lead.score, 60)
    
    def test_create_lead_with_low_score(self):
        """Testa criação de lead com score baixo (não qualificado)."""
        lead = Lead.objects.create(
            full_name="João Santos",
            case_type="OTHER",
            contact_info="joao@example.com",
            score=40,
            is_qualified=False
        )
        
        self.assertFalse(lead.is_qualified)
        self.assertLessEqual(lead.score, 60)


class WhatsAppNotificationTestCase(TestCase):
    """Testes do serviço de notificação WhatsApp."""
    
    def test_mock_notification_success(self):
        """Testa envio de notificação via mock provider."""
        lead = Lead.objects.create(
            full_name="Test Lead",
            case_type="LIPEDEMA",
            contact_info="(19) 99999-8888",
            score=80,
            is_qualified=True,
            triage_data={
                'negativa': 'sim',
                'description': 'Caso urgente de lipedema'
            }
        )
        
        service = WhatsAppNotificationService(provider='mock')
        result = service.send_lead_notification(lead)
        
        self.assertTrue(result)
    
    def test_message_formatting(self):
        """Testa formatação da mensagem WhatsApp."""
        lead = Lead.objects.create(
            full_name="Ana Costa",
            case_type="SUPER",
            contact_info="(11) 98765-4321",
            score=85,
            is_qualified=True,
            triage_data={
                'urgencia': 'urgente',
                'description': 'Superendividamento crítico'
            }
        )
        
        service = WhatsAppNotificationService(provider='mock')
        message = service._format_lead_message(lead)
        
        self.assertIn("Ana Costa", message)
        self.assertIn("SUPERENDIVIDAMENTO", message)
        self.assertIn("85/100", message)
        self.assertIn("ALTA PRIORIDADE", message)


class TriageSessionTestCase(TestCase):
    """Testes de sessão de triagem."""
    
    def test_create_triage_session(self):
        """Testa criação de sessão de triagem."""
        session = TriageSession.objects.create(
            session_id="test-session-123",
            current_step=1,
            temp_data={
                'name': 'Test User',
                'case_type': 'LIPEDEMA'
            }
        )
        
        self.assertEqual(session.session_id, "test-session-123")
        self.assertEqual(session.current_step, 1)
        self.assertIn('name', session.temp_data)


@pytest.mark.django_db
class TestIntakeFlow:
    """Testes de integração do fluxo completo de intake."""
    
    def test_complete_intake_flow_qualified_lead(self):
        """Testa fluxo completo: triagem → lead → notificação."""
        # 1. Criar sessão de triagem
        session = TriageSession.objects.create(
            session_id="integration-test-001",
            temp_data={
                'name': 'Carlos Oliveira',
                'case_type': 'LIPEDEMA'
            }
        )
        
        # 2. Simular dados do step 2
        session.temp_data.update({
            'negativa': 'sim',
            'contact': '(19) 97777-6666'
        })
        session.save()
        
        # 3. Criar lead
        lead = Lead.objects.create(
            full_name=session.temp_data['name'],
            case_type=session.temp_data['case_type'],
            contact_info=session.temp_data['contact'],
            triage_data=session.temp_data,
            score=70,
            is_qualified=True
        )
        
        # 4. Enviar notificação
        service = WhatsAppNotificationService(provider='mock')
        result = service.send_lead_notification(lead)
        
        # Validações
        assert lead.is_qualified is True
        assert lead.score > 60
        assert result is True
        assert Lead.objects.count() == 1
