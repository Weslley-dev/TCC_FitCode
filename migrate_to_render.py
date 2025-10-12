#!/usr/bin/env python
"""
Script para migrar dados do PostgreSQL local para o Render
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
from aparelhos.models import Grupo_muscular, Aparelho, Feedback, Visualizacao
from accounts.models import UserProfile

def migrate_to_render():
    print("🚀 Migrando dados para o Render...")
    
    try:
        # 1. Fazer dump dos dados locais
        print("📦 Fazendo backup dos dados locais...")
        call_command('dumpdata', '--natural-foreign', '--natural-primary', '--output=render_data.json')
        
        # 2. Verificar dados locais
        print("📊 Dados locais:")
        print(f"  👥 Usuários: {User.objects.count()}")
        print(f"  💪 Grupos: {Grupo_muscular.objects.count()}")
        print(f"  🏋️ Aparelhos: {Aparelho.objects.count()}")
        print(f"  💬 Feedbacks: {Feedback.objects.count()}")
        print(f"  👁️ Visualizações: {Visualizacao.objects.count()}")
        
        print("✅ Backup criado: render_data.json")
        print("📝 Próximos passos:")
        print("1. Configure a variável DATABASE_URL no Render")
        print("2. Faça deploy do código")
        print("3. Execute: python manage.py loaddata render_data.json")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    migrate_to_render()
