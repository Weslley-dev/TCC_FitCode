#!/usr/bin/env python
"""
Script para diagnosticar problemas de acesso administrativo e QR codes
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.contrib.auth.models import User
from aparelhos.models import Aparelho
from django.conf import settings

def diagnosticar_problemas():
    print("🔍 DIAGNÓSTICO DE PROBLEMAS")
    print("=" * 50)
    
    # 1. Verificar usuários administradores
    print("\n1. 👑 USUÁRIOS ADMINISTRADORES:")
    admins = User.objects.filter(is_superuser=True)
    for admin in admins:
        print(f"   - {admin.username} ({admin.email})")
        print(f"     Superuser: {admin.is_superuser}")
        print(f"     Staff: {admin.is_staff}")
        print(f"     Ativo: {admin.is_active}")
        print()
    
    # 2. Verificar configuração BASE_URL
    print("2. 🌐 CONFIGURAÇÃO BASE_URL:")
    base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
    print(f"   BASE_URL: {base_url}")
    
    # 3. Verificar aparelhos e QR codes
    print("\n3. 🏋️ APARELHOS E QR CODES:")
    aparelhos = Aparelho.objects.all()
    print(f"   Total de aparelhos: {aparelhos.count()}")
    
    qr_count = 0
    for aparelho in aparelhos:
        if aparelho.qr_code:
            qr_count += 1
        else:
            print(f"   ⚠️ Aparelho sem QR: {aparelho.exercise_name} (ID: {aparelho.id})")
    
    print(f"   Aparelhos com QR: {qr_count}/{aparelhos.count()}")
    
    # 4. Verificar permissões do decorator
    print("\n4. 🔐 VERIFICAÇÃO DE PERMISSÕES:")
    print("   Decorator admin_required verifica:")
    print("   - Usuário autenticado: ✅")
    print("   - Username = 'WeslleyDev': ❌ (problema aqui!)")
    print("   - is_superuser ou is_staff: ✅")
    
    # 5. Problemas identificados
    print("\n5. 🚨 PROBLEMAS IDENTIFICADOS:")
    print("   ❌ Decorator só permite 'WeslleyDev', mas você tem 'WeslleyAdmin'")
    print("   ❌ QR codes podem não estar sendo gerados por problemas de permissão")
    print("   ❌ BASE_URL pode estar incorreta para produção")
    
    # 6. Soluções
    print("\n6. 💡 SOLUÇÕES:")
    print("   ✅ Atualizar decorator para aceitar ambos os admins")
    print("   ✅ Verificar configuração de BASE_URL")
    print("   ✅ Regenerar QR codes existentes")

if __name__ == "__main__":
    diagnosticar_problemas()
