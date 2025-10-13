#!/usr/bin/env python
"""
Script para testar conexão com PostgreSQL do Render
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User

def test_postgres_connection():
    print("🔍 Testando conexão com PostgreSQL do Render...")
    print("=" * 50)
    
    try:
        # Testar conexão
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Conexão com PostgreSQL OK!")
            print(f"📊 Versão: {version}")
        
        # Verificar dados
        user_count = User.objects.count()
        print(f"\n📊 Dados no banco:")
        print(f"👥 Usuários: {user_count}")
        
        if user_count > 0:
            print("📋 Lista de usuários:")
            for user in User.objects.all()[:5]:
                print(f"  - {user.username} ({user.email}) - {'Admin' if user.is_superuser else 'Usuário'}")
            if user_count > 5:
                print(f"  ... e mais {user_count - 5} usuários")
        else:
            print("⚠️ Nenhum usuário encontrado - dados precisam ser migrados")
        
        print("\n🎉 PostgreSQL configurado corretamente!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

if __name__ == "__main__":
    test_postgres_connection()
