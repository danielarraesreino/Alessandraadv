from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Sends a test email to verify SMTP configuration.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            required=True,
            help='Recipient email address'
        )

    def handle(self, *args, **options):
        recipient = options['to']
        subject = 'Teste de Configuração de Email - Alessandra Antigravity'
        message = (
            'Olá,\n\n'
            'Este é um email de teste enviado pelo sistema Django para verificar a configuração SMTP.\n\n'
            'Se você recebeu esta mensagem, o envio de emails está funcionando corretamente via Google SMTP.\n\n'
            'Atenciosamente,\n'
            'Alessandra Antigravity System'
        )
        
        self.stdout.write(f"Tentando enviar email para {recipient} usando {settings.EMAIL_BACKEND}...")
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Sucesso! Email enviado para {recipient}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Falha ao enviar email: {e}'))
