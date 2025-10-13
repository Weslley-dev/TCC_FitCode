#!/usr/bin/env python
"""
Script para configurar PostgreSQL no Render.com
Execute este script para migrar do SQLite para PostgreSQL
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

def setup_postgres():
    print("🐘 Configurando PostgreSQL no Render...")
    
    try:
        # Verificar se estamos no Render
        if not os.environ.get('RENDER'):
            print("⚠️ Este script deve ser executado no ambiente Render")
            return
        
        # Verificar se já existe DATABASE_URL
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL não configurado no Render")
            print("📝 Configure uma variável de ambiente DATABASE_URL no painel do Render")
            return
        
        print(f"✅ DATABASE_URL encontrado: {database_url[:20]}...")
        
        # Fazer backup dos dados atuais (SQLite)
        print("💾 Fazendo backup dos dados atuais...")
        call_command('dumpdata', 
                    'auth.user', 
                    'accounts.userprofile', 
                    'aparelhos.aparelho',
                    'aparelhos.grupo_muscular',
                    'aparelhos.feedback',
                    'aparelhos.visualizacao',
                    '--indent', '2',
                    '--output', 'backup_sqlite.json')
        
        # Aplicar migrações no PostgreSQL
        print("🔄 Aplicando migrações no PostgreSQL...")
        call_command('migrate')
        
        # Restaurar dados no PostgreSQL
        print("📥 Restaurando dados no PostgreSQL...")
        call_command('loaddata', 'backup_sqlite.json')
        
        # Verificar dados
        user_count = User.objects.count()
        print(f"✅ Dados migrados com sucesso!")
        print(f"👥 Usuários no PostgreSQL: {user_count}")
        
        # Listar usuários
        for user in User.objects.all()[:5]:  # Mostrar apenas os primeiros 5
            print(f"  - {user.username} ({user.email})")
        
        if user_count > 5:
            print(f"  ... e mais {user_count - 5} usuários")
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_postgres()
