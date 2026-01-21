"""
Script SIMPLIFICADO para criar usuário de avaliação "manus" com permissões read-only.

Uso:
    python scripts/create_manus_readonly.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.models import User, Group, Permission

def create_readonly_group():
    """Cria grupo com permissões apenas de visualização"""
    group, created = Group.objects.get_or_create(name='ReadOnly_Evaluators')
    
    if created or group.permissions.count() == 0:
        # Adicionar apenas permissões "view_*" para todos os models
        view_permissions = Permission.objects.filter(codename__startswith='view_')
        group.permissions.set(view_permissions)
        print(f"✅ Grupo 'ReadOnly_Evaluators' criado com {view_permissions.count()} permissões de visualização")
    else:
        print(f"✅ Grupo 'ReadOnly_Evaluators' já existeim com {group.permissions.count()} permissões")
    
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
        print(f"✅ Usuário '{username}' criado com sucesso!")
    else:
        # Atualizar senha se já existe
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = False
        user.save()
        print(f"✅ Usuário '{username}' atualizado (senha resetada)!")
    
    # Adicionar ao grupo ReadOnly
    readonly_group = create_readonly_group()
    user.groups.add(readonly_group)
    user.save()
    
    return user

def main():
    print("\n" + "="*70)
    print(" 🔐 CRIANDO USUÁRIO AVALIADOR - MODO READ-ONLY")
    print("="*70 + "\n")
    
    user = create_manus_user()
    
    print("\n" + "="*70)
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║         CREDENCIAIS DE ACESSO - MODO AVALIAÇÃO (READ-ONLY)      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  👤 Usuário:  manus                                             ║
║  🔑 Senha:    Manus@Avaliador2026                               ║
║  📧 Email:    manus.avaliador@alessandradonadon.adv.br          ║
║                                                                  ║
║  🛡️  Tipo:     SOMENTE LEITURA (Read-Only)                      ║
║              - Pode visualizar TUDO                             ║
║              - NÃO pode editar/adicionar/deletar                ║
║              - NÃO pode alterar configurações                   ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  🌐 URLs de Acesso (Local):                                      ║
║                                                                  ║
║   http://localhost:8000/admin/                                  ║
║       └─ Admin Django (visualização)                            ║
║                                                                  ║
║   http://localhost:8000/portal-admin/                           ║
║       └─ Portal Administrativo                                  ║
║                                                                  ║
║   http://localhost:8000/portal-admin/dashboard/                 ║
║       └─ Dashboard de Métricas                                  ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  🚀 URLs de Acesso (Produção - acess quando deploy for feito):   ║
║                                                                  ║
║   https://web-production-36079.up.railway.app/admin/            ║
║   https://web-production-36079.up.railway.app/portal-admin/     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

✅ SETUP COMPLETO!

O usuário 'manus' pode agora:
  ✅ Fazer login no sistema (local ou produção)
  ✅ Visualizar todos os dados (clientes, leads, casos, finanças)
  ✅ Acessar o dashboard e relatórios
  ✅ Testar toda a interface sem risco
  ❌ NÃO pode editar, adicionar ou deletar dados
  ❌ NÃO pode alterar configurações do sistema
  ❌ NÃO pode acessar configurações administrativas críticas

IMPORTANTE: Os dados de exemplo podem ser populados manualmente
através do Portal Admin após fazer login com as credenciais acima.
""")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
