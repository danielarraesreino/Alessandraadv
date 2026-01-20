"""
WhatsApp Notification Service

Envia notificações de leads qualificados para o WhatsApp decisor.
Suporta múltiplos provedores: Mock (testing), Twilio, Evolution API.
"""
import logging
from typing import Optional
from django.conf import settings

logger = logging.getLogger(__name__)


class WhatsAppNotificationService:
    """
    Serviço de notificação WhatsApp para leads qualificados.
    """
    
    def __init__(self, provider: str = 'mock'):
        """
        Args:
            provider: 'mock', 'twilio', ou 'evolution'
        """
        self.provider = provider
        self.decisor_number = getattr(settings, 'WHATSAPP_DECISOR_NUMBER', '+5519988014465')
    
    def send_lead_notification(self, lead) -> bool:
        """
        Envia notificação de lead qualificado.
        
        Args:
            lead: Instância do modelo Lead
            
        Returns:
            bool: True se enviado com sucesso
        """
        message = self._format_lead_message(lead)
        
        if self.provider == 'mock':
            return self._send_mock(message, lead)
        
        # Only send real notifications for Score > 60
        if lead.score < 60:
            logger.info(f"Lead {lead.id} score {lead.score} too low for WhatsApp notification")
            return False

        if self.provider == 'twilio':
            return self._send_twilio(message)
        elif self.provider == 'evolution':
            return self._send_evolution(message)
    
    def _format_lead_message(self, lead) -> str:
        """Formata a mensagem de notificação com linguagem profissional."""
        priority_label = "ALTA PRIORIDADE" if lead.is_qualified else "Prioridade Padrão"
        
        message = f"""
*NOVO LEAD - {lead.get_case_type_display().upper()}*
{priority_label}

Nome: {lead.full_name}
Contato: {lead.contact_info}
Score de Qualificação: {lead.score}/100
"""
        
        if lead.is_qualified:
            message += "\nStatus: QUALIFICADO PARA ATENDIMENTO\n"
        
        message += "\nDados da Triagem:"
        
        # Adiciona dados específicos da triagem
        if lead.triage_data:
            for key, value in lead.triage_data.items():
                if key not in ['name', 'case_type', 'session_id']:
                    formatted_key = key.replace('_', ' ').title()
                    message += f"\n- {formatted_key}: {value}"
        
        message += f"\n\nRecebido via site em {lead.created_at.strftime('%d/%m/%Y às %H:%M')}"
        
        return message.strip()
    
    def _send_mock(self, message: str, lead) -> bool:
        """Mock provider para testes."""
        logger.info(f"[MOCK WhatsApp] Enviando para {self.decisor_number}")
        logger.info(f"[MOCK WhatsApp] Mensagem:\n{message}")
        
        # Simula envio bem-sucedido
        print("\n" + "="*60)
        print("📱 MOCK WHATSAPP NOTIFICATION")
        print("="*60)
        print(f"Para: {self.decisor_number}")
        print(f"Lead ID: {lead.id}")
        print("-"*60)
        print(message)
        print("="*60 + "\n")
        
        return True
    
    def _send_twilio(self, message: str) -> bool:
        """Envia via Twilio API."""
        try:
            from twilio.rest import Client
            
            account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
            auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
            from_number = getattr(settings, 'TWILIO_WHATSAPP_NUMBER', None)
            
            if not all([account_sid, auth_token, from_number]):
                logger.error("Credenciais Twilio não configuradas")
                return False
            
            client = Client(account_sid, auth_token)
            
            message_obj = client.messages.create(
                from_=f'whatsapp:{from_number}',
                body=message,
                to=f'whatsapp:{self.decisor_number}'
            )
            
            logger.info(f"WhatsApp enviado via Twilio: {message_obj.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar via Twilio: {e}")
            return False
    
    def _send_evolution(self, message: str) -> bool:
        """Envia via Evolution API."""
        try:
            import requests
            
            api_url = getattr(settings, 'EVOLUTION_API_URL', None)
            api_key = getattr(settings, 'EVOLUTION_API_KEY', None)
            instance = getattr(settings, 'EVOLUTION_INSTANCE', None)
            
            if not all([api_url, api_key, instance]):
                logger.error("Credenciais Evolution API não configuradas")
                return False
            
            response = requests.post(
                f"{api_url}/message/sendText/{instance}",
                headers={
                    'apikey': api_key,
                    'Content-Type': 'application/json'
                },
                json={
                    'number': self.decisor_number.replace('+', ''),
                    'text': message
                },
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"WhatsApp enviado via Evolution API")
                return True
            else:
                logger.error(f"Erro Evolution API: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao enviar via Evolution: {e}")
            return False
