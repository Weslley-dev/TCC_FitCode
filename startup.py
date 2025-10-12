#!/usr/bin/env python
"""
Script de inicialização para Render.com
Executa migrações e cria dados iniciais
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    django.setup()
    
    print("🚀 Iniciando configuração do Render...")
    
    # Executar migrações
    print("📊 Executando migrações...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        print("✅ Migrações executadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro nas migrações: {e}")
        sys.exit(1)
    
    # Verificar se as tabelas foram criadas
    try:
        user_count = User.objects.count()
        print(f"👥 Usuários no banco: {user_count}")
    except Exception as e:
        print(f"❌ Erro ao verificar banco: {e}")
        sys.exit(1)
    
    # Criar superusuário se não existir
    if not User.objects.filter(username='WeslleyDev').exists():
        print("👤 Criando superusuário...")
        try:
            User.objects.create_superuser(
                username='WeslleyDev',
                email='weslley@example.com',
                password='admin123',
                first_name='Weslley',
                last_name='Developer'
            )
            print("✅ Superusuário criado: WeslleyDev / admin123")
        except Exception as e:
            print(f"❌ Erro ao criar superusuário: {e}")
    
    # Coletar arquivos estáticos
    print("📁 Coletando arquivos estáticos...")
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Arquivos estáticos coletados!")
    except Exception as e:
        print(f"❌ Erro ao coletar estáticos: {e}")
    
    print("🎉 Configuração concluída com sucesso!")
