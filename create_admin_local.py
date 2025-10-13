#!/usr/bin/env python
"""
Script para criar superusuário localmente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    print("👤 Criando superusuário WeslleyAdmin...")
    
    try:
        # Verificar se já existe
        if User.objects.filter(username='WeslleyAdmin').exists():
            print("⚠️ Usuário WeslleyAdmin já existe. Atualizando...")
            user = User.objects.get(username='WeslleyAdmin')
            user.set_password('Admin123!')
            user.email = 'weslleypereira307@gmail.com'
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            print("✅ Usuário WeslleyAdmin atualizado!")
        else:
            # Criar novo usuário
            user = User.objects.create_user(
                username='WeslleyAdmin',
                email='weslleypereira307@gmail.com',
                password='Admin123!',
                first_name='Weslley',
                last_name='Admin',
                is_superuser=True,
                is_staff=True,
                is_active=True
            )
            print("✅ Usuário WeslleyAdmin criado!")

        # Verificar dados
        user_check = User.objects.get(username='WeslleyAdmin')
        print("📋 Dados do superusuário:")
        print(f"  👤 Usuário: {user_check.username}")
        print(f"  📧 E-mail: {user_check.email}")
        print(f"  🔑 Senha: Admin123!")
        print(f"  🔐 Superusuário: {user_check.is_superuser}")
        print(f"  👨‍💼 Staff: {user_check.is_staff}")
        print(f"  ✅ Ativo: {user_check.is_active}")
        
        # Fazer dump dos dados
        print("📦 Fazendo backup dos dados...")
        from django.core.management import call_command
        call_command('dumpdata', '--natural-foreign', '--natural-primary', '--output=admin_data.json')
        print("✅ Backup criado: admin_data.json")

    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_admin()