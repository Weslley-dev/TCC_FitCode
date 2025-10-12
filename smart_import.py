#!/usr/bin/env python
"""
Script para importar dados inteligentemente
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
from django.contrib.auth.models import User
from aparelhos.models import Aparelho, Feedback, Visualizacao, Grupo_muscular
from accounts.models import UserProfile

def smart_import():
    print("🚀 Importação inteligente de dados...")
    
    try:
        # Ler arquivo com codificação correta
        with open('railway_data.json', 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
        
        print(f"📊 Total de registros encontrados: {len(data)}")
        
        # Separar dados por modelo
        users_data = []
        profiles_data = []
        grupos_data = []
        aparelhos_data = []
        feedbacks_data = []
        visualizacoes_data = []
        
        for item in data:
            model = item.get('model', '')
            if model == 'auth.user':
                users_data.append(item)
            elif model == 'accounts.userprofile':
                profiles_data.append(item)
            elif model == 'aparelhos.grupo_muscular':
                grupos_data.append(item)
            elif model == 'aparelhos.aparelho':
                aparelhos_data.append(item)
            elif model == 'aparelhos.feedback':
                feedbacks_data.append(item)
            elif model == 'aparelhos.visualizacao':
                visualizacoes_data.append(item)
        
        print(f"👥 Usuários: {len(users_data)}")
        print(f"👤 Perfis: {len(profiles_data)}")
        print(f"🏋️ Grupos: {len(grupos_data)}")
        print(f"🏋️ Aparelhos: {len(aparelhos_data)}")
        print(f"💬 Feedbacks: {len(feedbacks_data)}")
        print(f"👀 Visualizações: {len(visualizacoes_data)}")
        
        # Importar grupos musculares primeiro
        if grupos_data:
            print("📤 Importando grupos musculares...")
            with open('grupos_temp.json', 'w', encoding='utf-8') as f:
                json.dump(grupos_data, f, ensure_ascii=False, indent=2)
            call_command('loaddata', 'grupos_temp.json')
            os.remove('grupos_temp.json')
        
        # Importar usuários
        if users_data:
            print("📤 Importando usuários...")
            with open('users_temp.json', 'w', encoding='utf-8') as f:
                json.dump(users_data, f, ensure_ascii=False, indent=2)
            call_command('loaddata', 'users_temp.json')
            os.remove('users_temp.json')
        
        # Importar perfis
        if profiles_data:
            print("📤 Importando perfis...")
            with open('profiles_temp.json', 'w', encoding='utf-8') as f:
                json.dump(profiles_data, f, ensure_ascii=False, indent=2)
            call_command('loaddata', 'profiles_temp.json')
            os.remove('profiles_temp.json')
        
        # Importar aparelhos
        if aparelhos_data:
            print("📤 Importando aparelhos...")
            with open('aparelhos_temp.json', 'w', encoding='utf-8') as f:
                json.dump(aparelhos_data, f, ensure_ascii=False, indent=2)
            call_command('loaddata', 'aparelhos_temp.json')
            os.remove('aparelhos_temp.json')
        
        # Importar feedbacks
        if feedbacks_data:
            print("📤 Importando feedbacks...")
            with open('feedbacks_temp.json', 'w', encoding='utf-8') as f:
                json.dump(feedbacks_data, f, ensure_ascii=False, indent=2)
            call_command('loaddata', 'feedbacks_temp.json')
            os.remove('feedbacks_temp.json')
        
        # Importar visualizações
        if visualizacoes_data:
            print("📤 Importando visualizações...")
            with open('visualizacoes_temp.json', 'w', encoding='utf-8') as f:
                json.dump(visualizacoes_data, f, ensure_ascii=False, indent=2)
            call_command('loaddata', 'visualizacoes_temp.json')
            os.remove('visualizacoes_temp.json')
        
        print("✅ DADOS IMPORTADOS COM SUCESSO!")
        
        # Verificar dados importados
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
    smart_import()
