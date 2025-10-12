#!/usr/bin/env python
"""
Script para corrigir codificação e importar dados
"""
import os
import sys
import django
import json
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.core.management import call_command

def fix_and_import():
    print("🚀 Corrigindo codificação e importando dados...")
    
    try:
        # Ler arquivo com codificação correta
        with open('railway_data.json', 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
        
        print(f"📊 Total de registros encontrados: {len(data)}")
        
        # Salvar com codificação correta
        with open('railway_fixed_utf8.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("✅ Arquivo corrigido salvo como railway_fixed_utf8.json")
        
        # Importar dados
        call_command('loaddata', 'railway_fixed_utf8.json')
        
        print("✅ DADOS IMPORTADOS COM SUCESSO!")
        
        # Verificar dados importados
        from django.contrib.auth.models import User
        from aparelhos.models import Aparelho, Feedback, Visualizacao
        
        user_count = User.objects.count()
        aparelho_count = Aparelho.objects.count()
        feedback_count = Feedback.objects.count()
        visualizacao_count = Visualizacao.objects.count()
        
        print(f"👥 Usuários: {user_count}")
        print(f"🏋️ Aparelhos: {aparelho_count}")
        print(f"💬 Feedbacks: {feedback_count}")
        print(f"👀 Visualizações: {visualizacao_count}")
        
        print("🌐 Acesse: https://tccfitcode-production.up.railway.app/admin/")
        print("👤 Username: WeslleyDev")
        print("🔑 Senha: WeslleyDev@dmin123")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == '__main__':
    fix_and_import()
