#!/usr/bin/env python3
import os
import subprocess
import sys
import time
from datetime import datetime

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    color = GREEN if level == "INFO" else (YELLOW if level == "WARN" else RED)
    print(f"{color}[{timestamp}] [{level}] {msg}{RESET}")

def run_command(command, cwd=None, exit_on_fail=True):
    log(f"Executando: {command}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            cwd=cwd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log(f"Erro ao executar comando: {command}", "ERROR")
        log(e.stderr, "ERROR")
        if exit_on_fail:
            sys.exit(1)
        return None

def check_git_status():
    status = run_command("git status --porcelain", exit_on_fail=False)
    if not status:
        log("Nenhuma alteração pendente para deploy.", "WARN")
        return False
    return True

def run_tests():
    log("Iniciando Quality Gates (Testes & Lint)...", "INFO")
    
    # 1. Django Check
    log("1/2 Verificando integridade do Django (manage.py check)...")
    run_command("python manage.py check")
    
    # 2. Testes Unitários
    log("2/2 Rodando testes unitários críticos (Intake/API)...")
    run_command("python manage.py test apps.intake.tests")
    
    log("✅ Todos os Quality Gates aprovados.", "INFO")

def deploy():
    # 1. Pré-Checks
    run_tests()
    
    if not check_git_status():
        confirm = input(f"{YELLOW}Repositório limpo. Deseja realizar um push vazio para forçar redeploy? (s/n): {RESET}")
        if confirm.lower() != 's':
            sys.exit(0)
        run_command("git commit --allow-empty -m 'chore: force redeploy via Agent'")
    else:
        # 2. Git Operations
        commit_msg = input(f"{GREEN}Digite a mensagem do commit: {RESET}")
        if not commit_msg:
            commit_msg = f"deploy: update via Agent at {datetime.now()}"
        
        run_command("git add .")
        run_command(f"git commit -m '{commit_msg}'")
    
    # 3. Push
    log("Enviando para o GitHub (Main)...", "INFO")
    run_command("git push origin main")
    
    log("🚀 Deploy iniciado! O servidor deve detectar o push em instantes.", "INFO")
    
    # 4. Logs (Optional)
    # Aqui poderíamos integrar com a CLI do provedor (Railway/Heroku)
    # Ex: run_command("railway logs --tail", exit_on_fail=False)
    log("Monitoramento de logs: Para ver os logs em tempo real, use a CLI do seu provedor ou o painel web.", "WARN")

if __name__ == "__main__":
    print(f"""
    {GREEN}
      🤖 Agent Deployer v1.0
      ======================
      Orquestração segura de deploy para Alessandra Antigravity
    {RESET}
    """)
    
    try:
        deploy()
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
