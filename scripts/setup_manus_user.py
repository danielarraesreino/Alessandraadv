"""
Script para criar usuário de avaliação "manus" com permissões read-only
e popular o sistema com dados de exemplo.

Uso:
    python scripts/setup_manus_user.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.clients.models import Client
from apps.intake.models import Lead, TriageSession
from apps.legal_cases.models import LegalCase
from apps.finance.models import AccountPayable, AccountReceivable

def create_readonly_group():
    """Cria grupo com permissões apenas de visualização"""
    group, created = Group.objects.get_or_create(name='ReadOnly_Evaluators')
    
    if created:
        # Adicionar apenas permissões "view_*" para todos os models
        view_permissions = Permission.objects.filter(codename__startswith='view_')
        group.permissions.set(view_permissions)
        print(f"✅ Grupo 'ReadOnly_Evaluators' criado com {view_permissions.count()} permissões")
    else:
        print(f"✅ Grupo 'ReadOnly_Evaluators' já existe")
    
    return group

def create_manus_user():
    """Cria usuário 'manus' com acesso read-only"""
    username = 'manus'
    password = 'Manus@Avaliador2026'
    email = 'manus.avaliador@alessandradonadon.adv.br'
    
    # Criar ou atualizar usuário
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': 'Manus',
            'last_name': 'Avaliador',
            'is_staff': True,  # Pode acessar admin
            'is_superuser': False,  # NÃO é superuser
            'is_active': True
        }
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f"✅ Usuário '{username}' criado com sucesso")
    else:
        # Atualizar senha se já existe
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = False
        user.save()
        print(f"✅ Usuário '{username}' atualizado")
    
    # Adicionar ao grupo ReadOnly
    readonly_group = create_readonly_group()
    user.groups.add(readonly_group)
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║         CREDENCIAIS DE ACESSO - MODO AVALIAÇÃO          ║
    ╠══════════════════════════════════════════════════════════╣
    ║  Usuário:  {username:<45} ║
    ║  Senha:    {password:<45} ║
    ║  Email:    {email:<45} ║
    ║  Tipo:     Read-Only (Somente Visualização){' '*14} ║
    ╠══════════════════════════════════════════════════════════╣
    ║  URLs de Acesso:                                          ║
    ║  - Admin Django:    /admin/                               ║
    ║  - Portal Admin:    /portal-admin/                        ║
    ║  - Dashboard:       /portal-admin/dashboard/              ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    return user

def populate_demo_clients():
    """Popula clientes de exemplo"""
    demo_clients = [
        {
            'name': 'Maria José Silva',
            'cpf_cnpj': '123.456.789-00',
            'email': 'maria.silva@email.com',
            'phone': '(19) 98765-4321',
            'address': 'Rua das Flores, 123 - Campinas/SP',
            'client_type': 'individual',
            'notes': 'Cliente desde 2024 - Caso de Lipedema'
        },
        {
            'name': 'João Pedro Santos',
            'cpf_cnpj': '987.654.321-00',
            'email': 'joao.santos@email.com',
            'phone': '(19) 99876-5432',
            'address': 'Av. Principal, 456 - Campinas/SP',
            'client_type': 'individual',
            'notes': 'Caso de Superendividamento - Em andamento'
        },
        {
            'name': 'Ana Carolina Oliveira',
            'cpf_cnpj': '456.789.123-00',
            'email': 'ana.oliveira@email.com',
            'phone': '(19) 97654-3210',
            'address': 'Rua dos Pinheiros, 789 - Campinas/SP',
            'client_type': 'individual',
            'notes': 'Negativa indevida de plano de saúde'
        }
    ]
    
    created_count = 0
    for client_data in demo_clients:
        client, created = Client.objects.get_or_create(
            cpf_cnpj=client_data['cpf_cnpj'],
            defaults=client_data
        )
        if created:
            created_count += 1
            print(f"  ✅ Cliente criado: {client.name}")
    
    print(f"✅ {created_count} clientes de exemplo criados")
    return Client.objects.all()

def populate_demo_leads():
    """Popula leads de exemplo"""
    demo_leads = [
        {
            'name': 'Paula Fernandes',
            'email': 'paula.fernandes@email.com',
            'phone': '(19) 96543-2109',
            'case_type': 'lipedema_health',
            'message': 'Plano de saúde negou cobertura de cirurgia de lipedema. Caso urgente.',
            'score': 85,
            'is_qualified': True,
            'status': 'new'
        },
        {
            'name': 'Roberto Costa',
            'email': 'roberto.costa@email.com',
            'phone': '(19) 95432-1098',
            'case_type': 'over_indebtedness',
            'message': 'Endividamento com múltiplos bancos. Preciso renegociar.',
            'score': 70,
            'is_qualified': True,
            'status': 'contacted'
        },
        {
            'name': 'Fernanda Lima',
            'email': 'fernanda.lima@email.com',
            'phone': '(19) 94321-0987',
            'case_type': 'lipedema_health',
            'message': 'Negativa de tratamento de lipedema pelo SUS.',
            'score': 60,
            'is_qualified': True,
            'status': 'new'
        },
        {
            'name': 'Carlos Eduardo',
            'email': 'carlos.eduardo@email.com',
            'phone': '(19) 93210-9876',
            'case_type': 'other',
            'message': 'Consulta sobre direitos trabalhistas.',
            'score': 30,
            'is_qualified': False,
            'status': 'unqualified'
        }
    ]
    
    created_count = 0
    for lead_data in demo_leads:
        lead, created = Lead.objects.get_or_create(
            email=lead_data['email'],
            defaults=lead_data
        )
        if created:
            created_count += 1
            print(f"  ✅ Lead criado: {lead.name} - Score: {lead.score}")
    
    print(f"✅ {created_count} leads de exemplo criados")
    return Lead.objects.all()

def populate_demo_cases(clients):
    """Popula casos jurídicos de exemplo"""
    if not clients.exists():
        print("⚠️  Nenhum cliente disponível para criar casos")
        return
    
    demo_cases = [
        {
            'client': clients[0] if len(clients) > 0 else None,
            'case_number': 'PROC-2024-001',
            'case_type': 'lipedema',
            'title': 'Ação de Obrigação de Fazer - Cobertura Lipedema',
            'description': 'Ação contra plano de saúde para cobertura de cirurgia de lipedema.',
            'status': 'in_progress',
            'priority': 'high'
        },
        {
            'client': clients[1] if len(clients) > 1 else None,
            'case_number': 'PROC-2024-002',
            'case_type': 'debt',
            'title': 'Procedimento de Superendividamento',
            'description': 'Renegociação de dívidas bancárias via Lei 14.181/2021.',
            'status': 'in_progress',
            'priority': 'medium'
        },
        {
            'client': clients[2] if len(clients) > 2 else None,
            'case_number': 'PROC-2023-045',
            'case_type': 'health',
            'title': 'Negativa Indevida de Plano de Saúde',
            'description': 'Ação por negativa de autorização de procedimento médico.',
            'status': 'completed',
            'priority': 'low'
        }
    ]
    
    created_count = 0
    for case_data in demo_cases:
        if case_data['client']:
            case, created = LegalCase.objects.get_or_create(
                case_number=case_data['case_number'],
                defaults=case_data
            )
            if created:
                created_count += 1
                print(f"  ✅ Caso criado: {case.case_number} - {case.title}")
    
    print(f"✅ {created_count} casos jurídicos de exemplo criados")

def populate_demo_finances():
    """Popula transações financeiras de exemplo - Contas a Pagar e Contas a Receber"""
    
    # Criar Contas a Pagar (Despesas do Escritório)
    demo_payables = [
        {
            'description': 'Aluguel do Escritório - Janeiro/2026',
            'supplier': 'Imobiliária Central',
            'amount': Decimal('3500.00'),
            'due_date': datetime.now().date() + timedelta(days=10),
            'status': 'PENDING',
            'category': 'OFFICE'
        },
        {
            'description': 'Software Jurídico - Assinatura Mensal',
            'supplier': 'LegalTech Solutions',
            'amount': Decimal('890.00'),
            'due_date': datetime.now().date() + timedelta(days=5),
            'status': 'PENDING',
            'category': 'SOFTWARE'
        },
        {
            'description': 'Custas Processuais - Caso PROC-2024-001',
            'supplier': 'Tribunal de Justiça SP',
            'amount': Decimal('1250.00'),
            'due_date': datetime.now().date() - timedelta(days=2),
            'status': 'PAID',
            'category': 'LEGAL_FEES'
        }
    ]
    
    payables_created = 0
    for payable_data in demo_payables:
        payable, created = AccountPayable.objects.get_or_create(
            description=payable_data['description'],
            due_date=payable_data['due_date'],
            defaults=payable_data
        )
        if created:
            payables_created += 1
            print(f"  ✅ Conta a Pagar criada: {payable.description} - R$ {payable.amount}")
    
    # Criar Contas a Receber (Honorários)
    cases = LegalCase.objects.all()
    demo_receivables = [
        {
            'legal_case': cases[0] if cases.exists() else None,
            'description': 'Honorários - Caso Lipedema Maria Silva',
            'client_name': 'Maria José Silva',
            'amount': Decimal('5000.00'),
            'due_date': datetime.now().date() + timedelta(days=15),
            'status': 'PENDING',
            'category': 'FEES'
        },
        {
            'legal_case': cases[1] if len(cases) > 1 else None,
            'description': 'Honorários - Superendividamento João Santos',
            'client_name': 'João Pedro Santos',
            'amount': Decimal('3500.00'),
            'due_date': datetime.now().date() - timedelta(days=5),
            'received_date': datetime.now().date(),
            'status': 'RECEIVED',
            'category': 'FEES'
        },
        {
            'legal_case': cases[2] if len(cases) > 2 else None,
            'description': 'Honorários de Êxito - Caso Ana Oliveira',
            'client_name': 'Ana Carolina Oliveira',
            'amount': Decimal('8000.00'),
            'due_date': datetime.now().date() - timedelta(days=30),
            'received_date': datetime.now().date() - timedelta(days=25),
            'status': 'RECEIVED',
            'category': 'SUCCESS_FEE'
        }
    ]
    
    receivables_created = 0
    for receivable_data in demo_receivables:
        receivable, created = AccountReceivable.objects.get_or_create(
            description=receivable_data['description'],
            defaults=receivable_data
        )
        if created:
            receivables_created += 1
            print(f"  ✅ Conta a Receber criada: {receivable.description} - R$ {receivable.amount}")
    
    print(f"✅ {payables_created} contas a pagar e {receivables_created} contas a receber criadas")

def main():
    print("\n" + "="*60)
    print("🚀 SETUP USUÁRIO AVALIADOR - MODO READ-ONLY")
    print("="*60 + "\n")
    
    print("📝 Passo 1: Criando usuário 'manus'...")
    user = create_manus_user()
    
    print("\n📝 Passo 2: Populando clientes de exemplo...")
    clients = populate_demo_clients()
    
    print("\n📝 Passo 3: Populando leads de exemplo...")
    leads = populate_demo_leads()
    
    print("\n📝 Passo 4: Populando casos jurídicos...")
    populate_demo_cases(clients)
    
    print("\n📝 Passo 5: Populando transações financeiras...")
    populate_demo_finances()
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETO!")
    print("="*60)
    print("""
    O usuário 'manus' pode agora:
    ✅ Fazer login no sistema
    ✅ Visualizar todos os dados (clientes, leads, casos, finanças)
    ✅ Acessar o dashboard e relatórios
    ❌ NÃO pode editar, adicionar ou deletar dados
    ❌ NÃO pode alterar configurações do sistema
    
    Use as credenciais acima para acessar!
    """)

if __name__ == '__main__':
    main()
