#!/usr/bin/env python
"""
Script para criar superusuário no Railway
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    print("🚀 Criando superusuário no Railway...")
    
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
    print("🌐 Acesse o admin em: https://tccfitcode-production.up.railway.app/admin/")

if __name__ == '__main__':
    create_superuser()
