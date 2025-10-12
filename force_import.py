#!/usr/bin/env python
"""
Script para forçar importação de dados no Railway
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Forçar ambiente Railway
os.environ['RAILWAY_ENVIRONMENT'] = 'True'

django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

def force_import():
    print("🚀 FORÇANDO IMPORTAÇÃO DE DADOS NO RAILWAY...")
    
    # Verificar se já existe
    if User.objects.filter(username='WeslleyDev').exists():
        print("✅ Superusuário já existe!")
    else:
        print("📤 Importando dados...")
        try:
            call_command('loaddata', 'railway_admin_data.json')
            print("✅ DADOS IMPORTADOS COM SUCESSO!")
        except Exception as e:
            print(f"❌ Erro: {e}")
            return
    
    # Verificar dados
    user_count = User.objects.count()
    print(f"👥 Total de usuários: {user_count}")
    
    # Verificar aparelhos
    try:
        from aparelhos.models import Aparelho
        aparelho_count = Aparelho.objects.count()
        print(f"🏋️ Total de aparelhos: {aparelho_count}")
    except:
        print("❌ Erro ao verificar aparelhos")
    
    print("🌐 Acesse: https://tccfitcode-production.up.railway.app/admin/")
    print("👤 Username: WeslleyDev")
    print("🔑 Senha: WeslleyDev@dmin123")

if __name__ == '__main__':
    force_import()
