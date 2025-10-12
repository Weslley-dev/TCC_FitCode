#!/usr/bin/env python
"""
Script para migrar dados do SQLite local para o PostgreSQL do Railway
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
from django.db import connection
from django.conf import settings

def migrate_data():
    print("🚀 Iniciando migração de dados para Railway...")
    
    # Verificar se estamos conectados ao banco correto
    print(f"📊 Banco atual: {settings.DATABASES['default']['ENGINE']}")
    print(f"📊 Host: {settings.DATABASES['default'].get('HOST', 'N/A')}")
    
    # Exportar dados do SQLite local
    print("📤 Exportando dados do SQLite local...")
    call_command('dumpdata', 
                '--natural-foreign', 
                '--natural-primary', 
                '--exclude=contenttypes', 
                '--exclude=auth.Permission',
                '--output=railway_data.json')
    
    print("✅ Dados exportados para railway_data.json")
    print("📤 Agora faça upload deste arquivo para o Railway e execute:")
    print("   python manage.py loaddata railway_data.json")
    print("")
    print("💡 Ou use o Railway CLI:")
    print("   railway run python manage.py loaddata railway_data.json")

if __name__ == '__main__':
    migrate_data()
