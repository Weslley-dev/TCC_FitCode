#!/usr/bin/env python
"""
Script para carregar dados no Render via shell
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.core.management import call_command

def load_data():
    print("🔄 Carregando dados no Render...")
    
    try:
        # Carregar dados do arquivo JSON
        call_command('loaddata', 'render_data.json')
        print("✅ Dados carregados com sucesso!")
        
        # Verificar dados
        from django.contrib.auth.models import User
        from aparelhos.models import Aparelho, Feedback, Visualizacao
        from accounts.models import UserProfile
        
        print(f"📊 Dados carregados:")
        print(f"  👥 Usuários: {User.objects.count()}")
        print(f"  🏋️ Aparelhos: {Aparelho.objects.count()}")
        print(f"  💬 Feedbacks: {Feedback.objects.count()}")
        print(f"  👁️ Visualizações: {Visualizacao.objects.count()}")
        print(f"  👤 Perfis: {UserProfile.objects.count()}")
        
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    load_data()
