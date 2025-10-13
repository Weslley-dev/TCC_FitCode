#!/usr/bin/env python
"""
Script para verificar a configuração do banco de dados
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.conf import settings
from django.db import connection
from django.contrib.auth.models import User

def check_database_config():
    print("🔍 Verificando configuração do banco de dados...")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    print("🌐 Variáveis de Ambiente:")
    print(f"  RENDER: {os.environ.get('RENDER', 'Não definido')}")
    print(f"  DATABASE_URL: {os.environ.get('DATABASE_URL', 'Não definido')[:50]}...")
    print()
    
    # Verificar configuração do Django
    print("⚙️ Configuração do Django:")
    db_config = settings.DATABASES['default']
    print(f"  Engine: {db_config['ENGINE']}")
    print(f"  Name: {db_config.get('NAME', 'N/A')}")
    print(f"  Host: {db_config.get('HOST', 'N/A')}")
    print(f"  Port: {db_config.get('PORT', 'N/A')}")
    print(f"  User: {db_config.get('USER', 'N/A')}")
    print()
    
    # Testar conexão
    print("🔌 Testando conexão:")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"  ✅ Conexão OK!")
            print(f"  📊 Versão do banco: {version}")
    except Exception as e:
        print(f"  ❌ Erro na conexão: {e}")
        return False
    
    # Verificar dados
    print("\n📊 Dados no banco:")
    try:
        user_count = User.objects.count()
        print(f"  👥 Usuários: {user_count}")
        
        if user_count > 0:
            print("  📋 Lista de usuários:")
            for user in User.objects.all()[:5]:
                print(f"    - {user.username} ({user.email}) - {'Admin' if user.is_superuser else 'Usuário'}")
            if user_count > 5:
                print(f"    ... e mais {user_count - 5} usuários")
        else:
            print("  ⚠️ Nenhum usuário encontrado")
            
    except Exception as e:
        print(f"  ❌ Erro ao consultar dados: {e}")
        return False
    
    print("\n" + "=" * 50)
    
    # Diagnóstico
    if 'postgresql' in db_config['ENGINE']:
        print("✅ PostgreSQL configurado corretamente!")
        if os.environ.get('DATABASE_URL'):
            print("✅ DATABASE_URL configurado!")
        else:
            print("⚠️ DATABASE_URL não encontrado - configure no painel do Render")
    else:
        print("⚠️ Usando SQLite - configure PostgreSQL para persistência")
    
    return True

if __name__ == "__main__":
    check_database_config()
