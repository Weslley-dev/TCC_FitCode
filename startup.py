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
    
    # Criar/atualizar superusuário
    print("👤 Configurando usuário administrador...")
    try:
        execute_from_command_line(['manage.py', 'create_admin'])
        print("✅ Administrador configurado!")
    except Exception as e:
        print(f"❌ Erro ao configurar administrador: {e}")
    
    # Criar dados de exemplo se não existirem
    from aparelhos.models import Aparelho
    if Aparelho.objects.count() == 0:
        print("🏋️ Criando dados de exemplo...")
        try:
            execute_from_command_line(['manage.py', 'create_sample_data'])
            print("✅ Dados de exemplo criados!")
        except Exception as e:
            print(f"❌ Erro ao criar dados de exemplo: {e}")
    
    # Coletar arquivos estáticos
    print("📁 Coletando arquivos estáticos...")
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Arquivos estáticos coletados!")
    except Exception as e:
        print(f"❌ Erro ao coletar estáticos: {e}")
    
    print("🎉 Configuração concluída com sucesso!")
