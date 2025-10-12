#!/usr/bin/env python
"""
Script para migrar dados do SQLite para PostgreSQL com mapeamento de IDs
"""
import os
import sys
import django
import sqlite3
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.contrib.auth.models import User
from aparelhos.models import Grupo_muscular, Aparelho, Feedback, Visualizacao
from accounts.models import UserProfile

def migrate_data():
    print("🔄 Iniciando migração SQLite → PostgreSQL com mapeamento...")
    
    # Conectar ao SQLite
    sqlite_db = sqlite3.connect('db.sqlite3')
    cursor = sqlite_db.cursor()
    
    try:
        # 1. Criar mapeamento de aparelhos
        print("🗺️ Criando mapeamento de aparelhos...")
        cursor.execute("SELECT id, exercise_name FROM aparelhos_aparelho")
        sqlite_aparelhos = cursor.fetchall()
        
        aparelho_mapping = {}
        for sqlite_id, exercise_name in sqlite_aparelhos:
            try:
                aparelho = Aparelho.objects.get(exercise_name=exercise_name)
                aparelho_mapping[sqlite_id] = aparelho.id
                print(f"  ✅ {exercise_name}: SQLite ID {sqlite_id} → PostgreSQL ID {aparelho.id}")
            except Aparelho.DoesNotExist:
                print(f"  ❌ Aparelho {exercise_name} não encontrado no PostgreSQL")
        
        # 2. Migrar feedbacks com mapeamento
        print("💬 Migrando feedbacks...")
        cursor.execute("""
            SELECT user_id, aparelho_id, rating, comment, created_at
            FROM aparelhos_feedback
        """)
        feedbacks = cursor.fetchall()
        
        for feedback_data in feedbacks:
            user_id, sqlite_aparelho_id, rating, comment, created_at = feedback_data
            
            try:
                user = User.objects.get(id=user_id)
                postgres_aparelho_id = aparelho_mapping.get(sqlite_aparelho_id)
                
                if postgres_aparelho_id:
                    aparelho = Aparelho.objects.get(id=postgres_aparelho_id)
                    
                    feedback = Feedback.objects.create(
                        user=user,
                        aparelho=aparelho,
                        rating=rating or 0,
                        comment=comment or '',
                        created_at=created_at
                    )
                    print(f"  ✅ Feedback do usuário {user.username} para {aparelho.exercise_name} migrado")
                else:
                    print(f"  ⏭️ Aparelho ID {sqlite_aparelho_id} não mapeado, pulando feedback")
            except Exception as e:
                print(f"  ❌ Erro ao migrar feedback: {e}")
        
        # 3. Migrar visualizações com mapeamento
        print("👁️ Migrando visualizações...")
        cursor.execute("""
            SELECT user_id, aparelho_id, count, last_clicked, viewed_at, updated_at
            FROM aparelhos_visualizacao
        """)
        visualizacoes = cursor.fetchall()
        
        for viz_data in visualizacoes:
            user_id, sqlite_aparelho_id, count, last_clicked, viewed_at, updated_at = viz_data
            
            try:
                user = User.objects.get(id=user_id)
                postgres_aparelho_id = aparelho_mapping.get(sqlite_aparelho_id)
                
                if postgres_aparelho_id:
                    aparelho = Aparelho.objects.get(id=postgres_aparelho_id)
                    
                    visualizacao = Visualizacao.objects.create(
                        user=user,
                        aparelho=aparelho,
                        count=count or 0,
                        last_clicked=last_clicked,
                        viewed_at=viewed_at,
                        updated_at=updated_at
                    )
                    print(f"  ✅ Visualização do usuário {user.username} para {aparelho.exercise_name} migrada")
                else:
                    print(f"  ⏭️ Aparelho ID {sqlite_aparelho_id} não mapeado, pulando visualização")
            except Exception as e:
                print(f"  ❌ Erro ao migrar visualização: {e}")
        
        print("🎉 Migração concluída com sucesso!")
        
        # Estatísticas finais
        print("\n📊 Estatísticas finais:")
        print(f"  👥 Usuários: {User.objects.count()}")
        print(f"  💪 Grupos musculares: {Grupo_muscular.objects.count()}")
        print(f"  🏋️ Aparelhos: {Aparelho.objects.count()}")
        print(f"  👤 Perfis: {UserProfile.objects.count()}")
        print(f"  💬 Feedbacks: {Feedback.objects.count()}")
        print(f"  👁️ Visualizações: {Visualizacao.objects.count()}")
        
    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")
        import traceback
        traceback.print_exc()
    finally:
        sqlite_db.close()

if __name__ == "__main__":
    migrate_data()
