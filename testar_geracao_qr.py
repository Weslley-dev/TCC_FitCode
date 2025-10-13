#!/usr/bin/env python
"""
Script para testar geração de QR codes
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from aparelhos.models import Aparelho
from django.conf import settings

def testar_geracao_qr():
    print("🧪 Testando geração de QR codes...")
    print("=" * 40)
    
    # Verificar configuração
    print(f"BASE_URL: {getattr(settings, 'BASE_URL', 'Não definido')}")
    
    # Testar com um aparelho
    aparelho = Aparelho.objects.first()
    if aparelho:
        print(f"\nTestando com: {aparelho.exercise_name}")
        print(f"ID: {aparelho.id}")
        print(f"QR atual: {aparelho.qr_code}")
        
        try:
            # Tentar gerar QR code
            print("\nGerando QR code...")
            aparelho.generate_qr_code()
            aparelho.save()
            print(f"QR após geração: {aparelho.qr_code}")
            
            if aparelho.qr_code:
                print("✅ QR code gerado com sucesso!")
            else:
                print("❌ Falha na geração do QR code")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ Nenhum aparelho encontrado")

if __name__ == "__main__":
    testar_geracao_qr()
