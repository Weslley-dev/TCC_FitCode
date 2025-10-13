#!/usr/bin/env python
"""
Script para configurar PostgreSQL no Render pago
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

def setup_render_postgres():
    print("🐘 Configurando PostgreSQL no Render pago...")
    print("=" * 50)
    
    # Verificar se estamos no Render
    if not os.environ.get('RENDER'):
        print("⚠️ Este script deve ser executado no ambiente Render")
        print("💡 Para testar localmente, defina: set RENDER=true")
        return
    
    # Verificar DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não configurado!")
        print("📝 Configure no painel do Render:")
        print("   1. Vá em Environment Variables")
        print("   2. Adicione: DATABASE_URL = (URL do seu banco PostgreSQL)")
        return
    
    print(f"✅ DATABASE_URL encontrado: {database_url[:30]}...")
    
    try:
        # Fazer backup dos dados atuais (se houver)
        print("\n💾 Fazendo backup dos dados atuais...")
        call_command('dumpdata', 
                    'auth.user', 
                    'accounts.userprofile', 
                    'aparelhos.aparelho',
                    'aparelhos.grupo_muscular',
                    'aparelhos.feedback',
                    'aparelhos.visualizacao',
                    '--indent', '2',
                    '--output', 'backup_before_postgres.json')
        print("✅ Backup criado: backup_before_postgres.json")
        
        # Aplicar migrações no PostgreSQL
        print("\n🔄 Aplicando migrações no PostgreSQL...")
        call_command('migrate')
        print("✅ Migrações aplicadas!")
        
        # Verificar se há dados para restaurar
        user_count = User.objects.count()
        print(f"\n📊 Usuários no PostgreSQL: {user_count}")
        
        if user_count == 0:
            print("📥 Restaurando dados do backup...")
            call_command('loaddata', 'backup_before_postgres.json')
            print("✅ Dados restaurados!")
        else:
            print("✅ Dados já existem no PostgreSQL!")
        
        # Verificar dados finais
        final_count = User.objects.count()
        print(f"\n🎉 Configuração concluída!")
        print(f"👥 Total de usuários: {final_count}")
        
        # Listar alguns usuários
        for user in User.objects.all()[:3]:
            print(f"  - {user.username} ({user.email})")
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_render_postgres()
