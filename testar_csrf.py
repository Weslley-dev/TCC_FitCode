#!/usr/bin/env python
"""
Script para testar configurações de CSRF
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.conf import settings
from django.test import Client

def testar_csrf():
    print("🔍 Testando configurações de CSRF...")
    print("=" * 40)
    
    # Verificar configurações
    print(f"CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}")
    print(f"CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
    print(f"SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
    print(f"DEBUG: {settings.DEBUG}")
    
    # Testar com cliente
    print("\n🧪 Testando URLs...")
    client = Client()
    
    # Testar admin
    response = client.get('/admin/')
    print(f"Admin GET status: {response.status_code}")
    
    # Testar login (POST)
    response = client.post('/admin/login/', {
        'username': 'WeslleyDev',
        'password': 'WeslleyDev@dmin123',
        'csrfmiddlewaretoken': client.get('/admin/').cookies.get('csrftoken', ''),
    })
    print(f"Admin POST status: {response.status_code}")
    
    if response.status_code in [200, 302]:
        print("✅ CSRF funcionando!")
    else:
        print("❌ Problema com CSRF")

if __name__ == "__main__":
    testar_csrf()
