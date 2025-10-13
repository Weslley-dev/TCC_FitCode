#!/usr/bin/env python
"""
Script de inicialização para o Render.com
Este script é executado automaticamente quando o serviço inicia
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

def startup_render():
    print("🚀 Iniciando aplicação no Render...")
    
    try:
        # Verificar se já existem usuários
        user_count = User.objects.count()
        print(f"👥 Usuários encontrados: {user_count}")
        
        if user_count == 0:
            print("📥 Nenhum usuário encontrado, restaurando dados...")
            
            # Tentar restaurar dados dos backups disponíveis
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
                # Criar superusuário padrão
                User.objects.create_superuser(
                    username='admin', 
                    email='admin@fitcode.com',
                    password='admin123'
                )
                print("✅ Superusuário criado: admin/admin123")
        else:
            print("✅ Dados já existem, continuando...")
        
        # Fazer backup dos dados atuais
        print("💾 Fazendo backup dos dados...")
        try:
            call_command('dumpdata', 
                        'auth.user', 
                        'accounts.userprofile', 
                        'aparelhos.aparelho',
                        'aparelhos.grupo_muscular',
                        'aparelhos.feedback',
                        'aparelhos.visualizacao',
                        '--indent', '2',
                        '--output', 'backup_data.json')
            print("✅ Backup criado: backup_data.json")
        except Exception as e:
            print(f"⚠️ Erro ao criar backup: {e}")
        
        print("🎉 Aplicação iniciada com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro na inicialização: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    startup_render()
