#!/usr/bin/env python
"""
Script para configurar PostgreSQL no Render automaticamente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

def configure_render_postgres():
    print("🚀 Configurando PostgreSQL no Render...")
    print("=" * 50)
    
    # DATABASE_URL do Render
    DATABASE_URL = "postgresql://tcc_fitcode_user:4oLdEYNWDYuJjrkz2TpbXCZXtzKjkSVX@dpg-d3m3ib56ubrc73egdfog-a.oregon-postgres.render.com/tcc_fitcode"
    
    # Verificar se estamos no Render
    if not os.environ.get('RENDER'):
        print("⚠️ Este script deve ser executado no ambiente Render")
        print("💡 Para testar localmente, defina: set RENDER=true")
        print(f"🔗 DATABASE_URL: {DATABASE_URL[:50]}...")
        return
    
    try:
        # Aplicar migrações
        print("🔄 Aplicando migrações no PostgreSQL...")
        call_command('migrate')
        print("✅ Migrações aplicadas!")
        
        # Verificar dados
        user_count = User.objects.count()
        print(f"\n📊 Dados no PostgreSQL:")
        print(f"👥 Usuários: {user_count}")
        
        if user_count > 0:
            print("✅ Dados já existem no PostgreSQL!")
            print("📋 Lista de usuários:")
            for user in User.objects.all()[:5]:
                print(f"  - {user.username} ({user.email}) - {'Admin' if user.is_superuser else 'Usuário'}")
            if user_count > 5:
                print(f"  ... e mais {user_count - 5} usuários")
        else:
            print("⚠️ Nenhum usuário encontrado - restaurando dados...")
            # Tentar restaurar dados dos backups
            backup_files = [
                'backup_data_atual.json',
                'backup_data.json', 
                'render_data.json',
                'admin_data.json'
            ]
            
            restored = False
            for backup_file in backup_files:
                if os.path.exists(backup_file):
                    print(f"🔄 Restaurando dados de {backup_file}...")
                    try:
                        call_command('loaddata', backup_file)
                        print(f"✅ Dados restaurados de {backup_file}!")
                        restored = True
                        break
                    except Exception as e:
                        print(f"⚠️ Erro ao restaurar {backup_file}: {e}")
                        continue
            
            if not restored:
                print("⚠️ Nenhum backup encontrado, criando dados iniciais...")
                # Deletar usuários existentes para evitar confusão
                User.objects.filter(is_superuser=True).delete()
                # Criar novo administrador
                User.objects.create_superuser(
                    username='admin', 
                    email='admin@fitcode.com',
                    password='admin123',
                    first_name='Admin',
                    last_name='FitCode'
                )
                print("✅ Superusuário criado: admin/admin123")
        
        print("\n🎉 PostgreSQL configurado com sucesso!")
        print("✅ Dados persistentes - nunca mais vão sumir!")
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    configure_render_postgres()
