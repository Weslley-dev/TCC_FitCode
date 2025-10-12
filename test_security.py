#!/usr/bin/env python
"""
Script para testar a segurança do sistema
"""
import os
import sys
import django

# Configurar Django primeiro
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_security():
    print("🔒 Testando segurança do sistema...")
    
    client = Client()
    
    # URLs administrativas que devem ser protegidas
    admin_urls = [
        '/aparelhos/',  # Lista de aparelhos (admin)
        '/aparelhos/novo/',  # Criar aparelho
        '/aparelhos/feedbacks/',  # Lista de feedbacks
        '/aparelhos/relatorios/',  # Relatórios
        '/clients/',  # Lista de clientes
        '/profile/admin/',  # Perfil admin
    ]
    
    # URLs de usuário comum
    user_urls = [
        '/aparelhos/user/',  # Lista de exercícios para usuários
        '/profile/',  # Perfil do usuário
    ]
    
    print("\n1. Testando acesso sem login...")
    for url in admin_urls + user_urls:
        response = client.get(url)
        if response.status_code == 302:  # Redirecionamento para login
            print(f"  ✅ {url}: Redirecionado para login (seguro)")
        else:
            print(f"  ❌ {url}: Status {response.status_code} (inseguro)")
    
    print("\n2. Testando acesso com usuário comum...")
    # Criar usuário comum para teste
    user, created = User.objects.get_or_create(
        username='teste_usuario',
        defaults={'email': 'teste@example.com', 'password': 'pbkdf2_sha256$test'}
    )
    
    client.force_login(user)
    
    for url in admin_urls:
        response = client.get(url)
        if response.status_code == 302:  # Redirecionamento
            print(f"  ✅ {url}: Usuário comum redirecionado (seguro)")
        else:
            print(f"  ❌ {url}: Usuário comum teve acesso (inseguro)")
    
    for url in user_urls:
        response = client.get(url)
        if response.status_code == 200:
            print(f"  ✅ {url}: Usuário comum tem acesso (correto)")
        else:
            print(f"  ❌ {url}: Usuário comum não tem acesso (erro)")
    
    print("\n3. Testando acesso com administrador...")
    # Usar o administrador real
    try:
        admin = User.objects.get(username='WeslleyDev')
        client.force_login(admin)
        
        for url in admin_urls:
            response = client.get(url)
            if response.status_code == 200:
                print(f"  ✅ {url}: Admin tem acesso (correto)")
            else:
                print(f"  ❌ {url}: Admin não tem acesso (erro)")
        
        for url in user_urls:
            response = client.get(url)
            if response.status_code == 200:
                print(f"  ✅ {url}: Admin tem acesso (correto)")
            else:
                print(f"  ❌ {url}: Admin não tem acesso (erro)")
                
    except User.DoesNotExist:
        print("  ❌ Usuário administrador não encontrado")
    
    print("\n🎯 Teste de segurança concluído!")

if __name__ == "__main__":
    test_security()
