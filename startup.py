#!/usr/bin/env python
"""
Script que executa automaticamente no Railway para importar dados
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

from django.core.management import call_command

def import_data():
    print("🚀 Railway Startup: Importando dados...")
    
    try:
        # Verificar se já foi importado
        from django.contrib.auth.models import User
        if User.objects.filter(username='WeslleyDev').exists():
            print("✅ Dados já importados!")
            return
        
        # Importar dados
        call_command('loaddata', 'railway_admin_data.json')
        print("✅ Dados importados com sucesso!")
        print("👤 Superusuário: WeslleyDev")
        print("📧 Email: weslleydevpereira@gmail.com")
        print("🔑 Senha: WeslleyDev@dmin123")
        
    except Exception as e:
        print(f"❌ Erro ao importar dados: {e}")

if __name__ == '__main__':
    import_data()
