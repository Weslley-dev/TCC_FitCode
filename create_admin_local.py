#!/usr/bin/env python
"""
Script para criar superusuário localmente e depois fazer push para Railway
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django para usar SQLite local
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Forçar uso do SQLite local
os.environ['RAILWAY_ENVIRONMENT'] = 'False'

django.setup()

from django.contrib.auth.models import User

def create_superuser():
    print("🚀 Criando superusuário localmente...")
    
    # Verificar se já existe
    if User.objects.filter(username='WeslleyDev').exists():
        print("❌ Usuário 'WeslleyDev' já existe!")
        return
    
    # Criar superusuário
    user = User.objects.create_superuser(
        username='WeslleyDev',
        email='weslleydevpereira@gmail.com',
        password='WeslleyDev@dmin123'
    )
    
    print("✅ Superusuário criado com sucesso!")
    print(f"👤 Username: {user.username}")
    print(f"📧 Email: {user.email}")
    print(f"🔑 Senha: WeslleyDev@dmin123")
    print("")
    print("📤 Agora vou exportar os dados para o Railway...")
    
    # Exportar dados
    from django.core.management import call_command
    call_command('dumpdata', 
                '--natural-foreign', 
                '--natural-primary', 
                '--exclude=contenttypes', 
                '--exclude=auth.Permission',
                '--output=railway_admin_data.json')
    
    print("✅ Dados exportados para railway_admin_data.json")
    print("🚀 Agora vou fazer push para o Railway...")

if __name__ == '__main__':
    create_superuser()
