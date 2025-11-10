#!/usr/bin/env python
"""
Script de preparação para deploy
Executa todas as verificações necessárias antes do deploy
"""
import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_file(filepath, description):
    """Verifica se um arquivo existe"""
    if Path(filepath).exists():
        print(f"✅ {description}: OK")
        return True
    else:
        print(f"❌ {description}: NÃO ENCONTRADO")
        return False

def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description}: OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}: ERRO")
        print(f"   {e.stderr}")
        return False

def main():
    print_header("VERIFICAÇÃO PRÉ-DEPLOY - BIBLIOTECA ONLINE")
    
    checks_passed = 0
    checks_total = 0
    
    # 1. Verificar arquivos essenciais
    print_header("1. Verificando arquivos essenciais")
    checks_total += 5
    if check_file("requirements.txt", "requirements.txt"):
        checks_passed += 1
    if check_file("Procfile", "Procfile"):
        checks_passed += 1
    if check_file("runtime.txt", "runtime.txt"):
        checks_passed += 1
    if check_file(".gitignore", ".gitignore"):
        checks_passed += 1
    if check_file(".env.example", ".env.example"):
        checks_passed += 1
    
    # 2. Verificar arquivo .env
    print_header("2. Verificando configurações de ambiente")
    checks_total += 1
    if Path(".env").exists():
        print("✅ Arquivo .env encontrado")
        checks_passed += 1
        print("⚠️  LEMBRE-SE: Nunca commite o arquivo .env!")
    else:
        print("⚠️  Arquivo .env não encontrado")
        print("   Copie .env.example para .env e configure:")
        print("   cp .env.example .env")
    
    # 3. Verificar Git
    print_header("3. Verificando Git")
    checks_total += 2
    if Path(".git").exists():
        print("✅ Repositório Git inicializado")
        checks_passed += 1
        
        # Verificar se há commits
        try:
            result = subprocess.run(["git", "log", "-1"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Há commits no repositório")
                checks_passed += 1
            else:
                print("⚠️  Nenhum commit encontrado. Execute:")
                print("   git add .")
                print('   git commit -m "Preparar para deploy"')
        except:
            print("⚠️  Não foi possível verificar commits")
    else:
        print("❌ Repositório Git não inicializado")
        print("   Execute: git init")
    
    # 4. Verificar Python/Django
    print_header("4. Verificando Django")
    checks_total += 3
    
    if run_command("python --version", "Python instalado"):
        checks_passed += 1
    
    if run_command("pip show django", "Django instalado"):
        checks_passed += 1
    
    # Verificar se manage.py existe
    if check_file("biblioteca_online/manage.py", "manage.py"):
        checks_passed += 1
    
    # 5. Testes básicos
    print_header("5. Executando verificações do Django")
    checks_total += 1
    os.chdir("biblioteca_online")
    if run_command("python manage.py check", "Django check"):
        checks_passed += 1
    os.chdir("..")
    
    # Resultado final
    print_header("RESULTADO DA VERIFICAÇÃO")
    percentage = (checks_passed / checks_total) * 100
    print(f"\n✅ Verificações passadas: {checks_passed}/{checks_total} ({percentage:.1f}%)")
    
    if checks_passed == checks_total:
        print("\n🎉 TUDO PRONTO PARA DEPLOY!")
        print("\n📝 Próximos passos:")
        print("   1. Configure suas variáveis de ambiente no .env")
        print("   2. Escolha uma plataforma (Heroku, Railway, Render)")
        print("   3. Siga as instruções no arquivo DEPLOY.md")
    elif percentage >= 80:
        print("\n⚠️  QUASE PRONTO - Resolva os problemas acima")
    else:
        print("\n❌ NÃO RECOMENDADO FAZER DEPLOY AINDA")
        print("   Resolva os problemas identificados primeiro")
    
    print("\n📖 Consulte DEPLOY.md para instruções detalhadas\n")

if __name__ == "__main__":
    main()
