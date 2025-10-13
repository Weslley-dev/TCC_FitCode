#!/usr/bin/env python
"""
Script para testar arquivos estáticos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.conf import settings
from django.test import Client

def testar_estaticos():
    print("🔍 Testando arquivos estáticos...")
    print("=" * 40)
    
    # Verificar configurações
    print(f"DEBUG: {settings.DEBUG}")
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    
    # Verificar se o diretório existe
    if os.path.exists(settings.STATIC_ROOT):
        print(f"✅ Diretório staticfiles existe")
        arquivos = os.listdir(settings.STATIC_ROOT)
        print(f"📁 Arquivos encontrados: {len(arquivos)}")
        
        # Verificar se tem admin
        admin_path = os.path.join(settings.STATIC_ROOT, 'admin')
        if os.path.exists(admin_path):
            print("✅ CSS do admin encontrado")
        else:
            print("❌ CSS do admin não encontrado")
    else:
        print("❌ Diretório staticfiles não existe")
    
    # Testar com cliente
    print("\n🧪 Testando URLs...")
    client = Client()
    
    # Testar admin
    response = client.get('/admin/')
    print(f"Admin status: {response.status_code}")
    
    # Testar arquivo estático
    response = client.get('/static/admin/css/base.css')
    print(f"CSS admin status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Arquivos estáticos funcionando!")
    else:
        print("❌ Problema com arquivos estáticos")

if __name__ == "__main__":
    testar_estaticos()
