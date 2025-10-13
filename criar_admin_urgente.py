#!/usr/bin/env python
"""
Script para criar/atualizar usuário administrador urgentemente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.contrib.auth.models import User

def criar_admin_urgente():
    print("🚨 CRIANDO ADMINISTRADOR URGENTE...")
    print("=" * 50)
    
    # Deletar usuários existentes para evitar confusão
    print("🧹 Limpando usuários existentes...")
    User.objects.filter(is_superuser=True).delete()
    
    # Criar novo administrador
    print("👤 Criando novo administrador...")
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@fitcode.com',
        password='admin123',
        first_name='Admin',
        last_name='FitCode'
    )
    
    print("✅ Administrador criado com sucesso!")
    print(f"👤 Username: {admin.username}")
    print(f"📧 Email: {admin.email}")
    print(f"🔑 Senha: admin123")
    print(f"✅ Ativo: {admin.is_active}")
    print(f"🔧 Superuser: {admin.is_superuser}")
    print(f"👨‍💼 Staff: {admin.is_staff}")
    
    print("\n🌐 ACESSO:")
    print("URL: https://tcc-fitcode-web.onrender.com/admin/login/")
    print("Usuário: admin")
    print("Senha: admin123")
    
    # Verificar se consegue fazer login
    from django.contrib.auth import authenticate
    user = authenticate(username='admin', password='admin123')
    if user:
        print("\n✅ Login testado com sucesso!")
    else:
        print("\n❌ Erro no login!")

if __name__ == "__main__":
    criar_admin_urgente()
