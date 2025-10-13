#!/usr/bin/env python
"""
Script para verificar QR codes
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from aparelhos.models import Aparelho

def verificar_qr_codes():
    print("🔍 Verificando QR Codes:")
    print("=" * 30)
    
    aparelhos = Aparelho.objects.all()
    print(f"Total de aparelhos: {aparelhos.count()}")
    print()
    
    qr_count = 0
    for aparelho in aparelhos:
        status = "✅" if aparelho.qr_code else "❌"
        print(f"{status} {aparelho.exercise_name} (ID: {aparelho.id})")
        if aparelho.qr_code:
            qr_count += 1
    
    print(f"\nResumo: {qr_count}/{aparelhos.count()} com QR codes")

if __name__ == "__main__":
    verificar_qr_codes()
