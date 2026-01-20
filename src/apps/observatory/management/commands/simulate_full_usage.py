from django.core.management import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
from apps.clients.models import Client
from apps.intake.models import Lead
from apps.legal_cases.models import LegalCase
from apps.finance.models import AccountReceivable, AccountPayable
from apps.observatory.models import HumanRightsCase
from apps.portals.models import CaseTimeline, ClientPortalAccess
import random
import secrets

class Command(BaseCommand):
    help = 'Popula todo o sistema (Leads, Clientes, Financeiro, Casos, Portal) com personas históricas para simulação de uso.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando Simulação Completa (Full Usage)...')

        # ... (personas list remains same)
        # Assuming personas list is defined above or inherited? 
        # Wait, replace_file_content replaces chunks. I need to be careful not to delete the personas list if I'm editing the whole file or a chunk.
        # I will replace the imports and the loop content.

        # Imports are at the top. I'll add them first.
        pass # Placeholder for thought process. I need to make sure I import at the top.

# RETRYING CAREFULLY


class Command(BaseCommand):
    help = 'Popula todo o sistema (Leads, Clientes, Financeiro, Casos) com personas históricas para simulação de uso.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando Simulação Completa (Full Usage)...')

        personas = [
            # Personas baseadas nos casos históricos
             {
                "name": "Vladimir Herzog",
                "email": "vladimir@herzog.org.br",
                "phone": "+55 11 99999-1975",
                "type": "PF",
                "case_title": "Ação Indenizatória - Danos Morais",
                "area": "CIVIL",
                "risk": "MEDIUM",
                "value": 500000.00,
                "desc": "Ação de reparação do Estado por violações ocorridas na década de 70.",
                "status": "ACTIVE",
                "lead_source": "Indicação",
                "lead_type": "OTHER"
            },
            {
                "name": "Família Rubens Paiva",
                "email": "contato@rubenspaiva.org",
                "phone": "+55 21 98888-1971",
                "type": "PF",
                "case_title": "Reconhecimento de Anistia Política",
                "area": "CIVIL",
                "risk": "LOW",
                "value": 1200000.00,
                "desc": "Pedido administrativo e judicial para reconhecimento formal de anistia.",
                "status": "ACTIVE",
                "lead_source": "Orgânico (Site)",
                "lead_type": "OTHER"
            },
            {
                "name": "Chico Mendes",
                "email": "chico@floresta.org",
                "phone": "+55 68 97777-1988",
                "type": "PJ", # Associação
                "case_title": "Tutela Proibitória - Proteção Ambiental",
                "area": "THIRD_SECTOR",
                "risk": "HIGH",
                "value": 0.00, # Ação de obrigação de fazer
                "desc": "Medida urgente para impedir desmatamento ilegal em reserva extrativista.",
                "status": "ACTIVE",
                 "lead_source": "WhatsApp Bot",
                "lead_type": "CULTURAL"
            },
             {
                "name": "Assoc. Eldorado dos Carajás",
                "email": "mst@eldorado.org",
                "phone": "+55 94 96666-1996",
                "type": "PJ",
                "case_title": "Ação Coletiva de Indenização",
                "area": "CIVIL",
                "risk": "MEDIUM",
                "value": 10000000.00,
                "desc": "Representação das famílias das vítimas em ação coletiva.",
                "status": "SUSPENDED",
                "lead_source": "Parceiro",
                "lead_type": "OTHER"
            },
            {
                "name": "Marielle Franco In Memoriam",
                "email": "instituto@marielle.org",
                "phone": "+55 21 95555-2018",
                "type": "PF",
                "case_title": "Acompanhamento de Inquérito Policial",
                "area": "CIVIL", # Assistente de Acusação
                "risk": "HIGH",
                "value": 0.00,
                "desc": "Atuação como assistente de acusação no tribunal do júri.",
                "status": "ACTIVE",
                "lead_source": "WhatsApp Bot",
                "lead_type": "OTHER"
            },
            {
                "name": "Amarildo de Souza",
                "email": "familia@amarildo.com",
                "phone": "+55 21 94444-2013",
                "type": "PF",
                "case_title": "Ação Declaratória de Ausência",
                "area": "CIVIL",
                "risk": "LOW",
                "value": 50000.00,
                "desc": "Regularização civil e previdenciária da família.",
                "status": "ARCHIVED",
                "lead_source": "Intake Form",
                "lead_type": "OTHER"
            },
            {
                "name": "Bruno Pereira",
                "email": "bruno@indigenistas.org",
                "phone": "+55 92 93333-2022",
                "type": "PF",
                "case_title": "Defesa em Processo Administrativo (FUNAI)",
                "area": "OTHER",
                "risk": "MEDIUM",
                "value": 0.00,
                "desc": "Defesa técnica contra exoneração arbitrária.",
                "status": "ARCHIVED", # Post mortem
                "lead_source": "LinkedIn",
                "lead_type": "OTHER"
            },
             {
                "name": "Comunidade de Paraisópolis",
                "email": "uniao@paraisopolis.org",
                "phone": "+55 11 92222-2019",
                "type": "PJ", # Associação de Moradores
                "case_title": "Consultoria Jurídica - Eventos Culturais",
                "area": "THIRD_SECTOR",
                "risk": "LOW",
                "value": 15000.00,
                "desc": "Regularização de alvarás para eventos comunitários.",
                "status": "ACTIVE",
                 "lead_source": "Indicação",
                "lead_type": "CULTURAL"
            },
            {
                "name": "Liderança Yanomami",
                "email": "lider@hutukara.org",
                "phone": "+55 95 91111-2023",
                "type": "PF",
                "case_title": "Denúncia Internacional - Direitos Humanos",
                "area": "HEALTH", # Saúde Indígena
                "risk": "HIGH",
                "value": 0.00,
                "desc": "Preparação de dossiê para a Corte Interamericana.",
                "status": "ANALYSIS",
                "lead_source": "WhatsApp Bot",
                "lead_type": "LIPEDEMA" # Uso criativo do tipo saúde
            },
            {
                "name": "Olga Benário",
                "email": "memoria@olga.org",
                "phone": "+55 21 90000-1936",
                "type": "PF",
                "case_title": "Inventário Extrajudicial",
                "area": "CIVIL",
                "risk": "LOW",
                "value": 200000.00,
                "desc": "Inventário de bens remanescentes da família.",
                "status": "ARCHIVED",
                "lead_source": "Arquivo Morto",
                "lead_type": "OTHER"
            },
             {
                "name": "João Pedro Mattos",
                "email": "joao@pedro.org",
                "phone": "+55 21 98989-2020",
                "type": "PF",
                "case_title": "Indenização por Danos Materiais",
                "area": "CIVIL",
                "risk": "MEDIUM",
                "value": 80000.00,
                "desc": "Reparação por danos ao imóvel durante operação.",
                "status": "ACTIVE",
                 "lead_source": "Intake Form",
                "lead_type": "OTHER"
            },
             {
                "name": "Genivaldo Santos",
                "email": "justica@genivaldo.org",
                "phone": "+55 79 97979-2022",
                "type": "PF",
                "case_title": "Pensão por Morte (Previdenciário)",
                "area": "CIVIL",
                "risk": "LOW",
                "value": 150000.00,
                "desc": "Requerimento de benefício para a viúva.",
                "status": "ACTIVE",
                "lead_source": "WhatsApp Bot",
                "lead_type": "OTHER"
            }
        ]

        today = timezone.now().date()

        for p in personas:
            # 1. Lead Generation (Simulando funil)
            # Metade vira cliente, mas todos começam como Lead
            lead, created = Lead.objects.get_or_create(
                full_name=p['name'],
                defaults={
                    "contact_info": p['phone'],
                    "case_type": p['lead_type'],
                    "source": p['lead_source'],
                    "triage_data": {"notes": f"Lead gerado via simulação. Caso: {p['desc']}"},
                    "score": random.randint(30, 95),
                    "is_qualified": True
                }
            )
            
            if created:
                self.stdout.write(f"Lead Criado: {p['name']}")

            # 2. Client Acquisition (Todos viram clientes para popular o dashboard)
            client_status = 'ACTIVE'
            if p['status'] == 'ARCHIVED':
                client_status = 'ARCHIVED'
            elif p['status'] == 'ANALYSIS':
                client_status = 'ONBOARDING'
            
            client, created = Client.objects.get_or_create(
                full_name=p['name'],
                defaults={
                    "cpf_cnpj": f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}",
                    "client_type": p['type'],
                    "phone": p['phone'],
                    "email": p['email'],
                    "status": client_status
                }
            )
            
            # Se já existia, garante update do status para refletir simulação
            if not created:
                client.status = client_status
                client.save()
            
            # Atualiza lead com External ID se convertido
            lead.external_id = f"CLI-{client.id}"
            lead.save()

            # 3. Case Creation
            legal_case, created = LegalCase.objects.get_or_create(
                client=client,
                title=p['case_title'],
                defaults={
                    "area": p['area'],
                    "risk_level": p['risk'],
                    "contingency_value": p['value'],
                    "description": p['desc'],
                    "status": p['status'],
                    "process_number": f"{random.randint(1000,9999)}.202{random.randint(0,5)}.8.26.0100"
                }
            )

            # 4. Finance Generation (Honorários e Despesas)
            if p['value'] > 0:
                # Recebíveis (Honorários)
                AccountReceivable.objects.create(
                    description=f"Honorários Iniciais - {p['name']}",
                    amount=max(p['value'] * 0.10, 2500.00), # 10% ou min 2500
                    due_date=today + timedelta(days=random.randint(-30, 30)),
                    category='FEES',
                    legal_case=legal_case,
                    client_name=client.full_name,
                    status=random.choice(['PENDING', 'RECEIVED'])
                )
                
            # Pagáveis (Custas do escritório aleatórias)
            if random.choice([True, False]):
                AccountPayable.objects.create(
                    description=f"Deslocamento/Custas - {p['case_title']}",
                    amount=random.uniform(50.00, 500.00),
                    due_date=today + timedelta(days=random.randint(-15, 15)),
                    category='LEGAL_FEES',
                    supplier="Uber/Cartório",
                    status=random.choice(['PENDING', 'PAID'])
                )

            # 5. Portal & Timeline Generation (A parte "Fluida/Humana")
            # Criar Timeline
            timeline, _ = CaseTimeline.objects.get_or_create(legal_case=legal_case)
            
            # Definir etapas baseado no status do caso
            stages_to_add = []
            if p['status'] == 'ARCHIVED':
                stages_to_add = ['INTAKE', 'ANALYSIS', 'PETITION', 'FILED', 'DECISION', 'CLOSED']
                timeline.current_stage = 'CLOSED'
            elif p['status'] == 'ACTIVE':
                stages_to_add = ['INTAKE', 'ANALYSIS', 'PETITION', 'FILED']
                timeline.current_stage = 'FILED'
            elif p['status'] == 'SUSPENDED':
                stages_to_add = ['INTAKE', 'ANALYSIS']
                timeline.current_stage = 'ANALYSIS'
            else: # ANALYSIS
                stages_to_add = ['INTAKE']
                timeline.current_stage = 'INTAKE'

            # Limpar milestones anteriores para evitar duplicação no re-run
            timeline.milestones = []
            
            base_date = p.get('created_at', timezone.now()) # Usar data fictícia se tivesse
            
            for i, stage in enumerate(stages_to_add):
                # Data progressiva
                milestone_date = today - timedelta(days=30 * (len(stages_to_add) - i))
                timeline.milestones.append({
                    'stage': stage,
                    'date': milestone_date.isoformat(),
                    'notes': f"Etapa {stage} concluída com sucesso.",
                    'updated_by': "Sistema"
                })
            
            timeline.save()

            # Gerar Token de Acesso
            token = secrets.token_urlsafe(16)
            portal_access, _ = ClientPortalAccess.objects.get_or_create(
                client=client,
                legal_case=legal_case,
                defaults={'access_token': token}
            )
            
            if _ or portal_access.access_token:
                 self.stdout.write(f"  > Portal Token ({p['name']}): {portal_access.access_token}")

        self.stdout.write(self.style.SUCCESS("Simulação 100% Concluída. Todos os módulos populados (incluindo Portals)."))
