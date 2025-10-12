#!/usr/bin/env python
"""
Script para migrar dados do SQLite para PostgreSQL
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
    print("🔄 Iniciando migração SQLite → PostgreSQL...")
    
    # Conectar ao SQLite
    sqlite_db = sqlite3.connect('db.sqlite3')
    cursor = sqlite_db.cursor()
    
    try:
        # 1. Migrar usuários
        print("👥 Migrando usuários...")
        cursor.execute("SELECT username, email, password, first_name, last_name, is_superuser, is_staff, is_active, date_joined FROM auth_user")
        users = cursor.fetchall()
        
        for user_data in users:
            username, email, password, first_name, last_name, is_superuser, is_staff, is_active, date_joined = user_data
            
            # Pular se já existe
            if User.objects.filter(username=username).exists():
                print(f"  ⏭️ Usuário {username} já existe, pulando...")
                continue
                
            user = User.objects.create_user(
                username=username,
                email=email,
                password='temp_password',  # Será alterado
                first_name=first_name or '',
                last_name=last_name or '',
                is_superuser=bool(is_superuser),
                is_staff=bool(is_staff),
                is_active=bool(is_active)
            )
            
            # Restaurar senha original (hash)
            user.password = password
            user.save()
            print(f"  ✅ Usuário {username} migrado")
        
        # 2. Migrar grupos musculares
        print("💪 Migrando grupos musculares...")
        cursor.execute("SELECT name FROM aparelhos_grupo_muscular")
        grupos = cursor.fetchall()
        
        for grupo_data in grupos:
            name = grupo_data[0]
            if not Grupo_muscular.objects.filter(name=name).exists():
                Grupo_muscular.objects.create(name=name)
                print(f"  ✅ Grupo {name} migrado")
            else:
                print(f"  ⏭️ Grupo {name} já existe, pulando...")
        
        # 3. Migrar aparelhos
        print("🏋️ Migrando aparelhos...")
        cursor.execute("""
            SELECT exercise_name, grupo_muscular_id, instructions, image, video, qr_code
            FROM aparelhos_aparelho
        """)
        aparelhos = cursor.fetchall()
        
        for aparelho_data in aparelhos:
            exercise_name, grupo_id, instructions, image, video, qr_code = aparelho_data
            
            try:
                grupo = Grupo_muscular.objects.get(id=grupo_id)
                
                aparelho = Aparelho.objects.create(
                    exercise_name=exercise_name,
                    grupo_muscular=grupo,
                    instructions=instructions or '',
                    image=image if image else None,
                    video=video if video else None,
                    qr_code=qr_code if qr_code else None
                )
                print(f"  ✅ Aparelho {exercise_name} migrado")
            except Exception as e:
                print(f"  ❌ Erro ao migrar aparelho {exercise_name}: {e}")
        
        # 4. Migrar perfis de usuário
        print("👤 Migrando perfis de usuário...")
        cursor.execute("""
            SELECT user_id, profile_picture, bio, phone, birth_date, created_at, updated_at
            FROM accounts_userprofile
        """)
        perfis = cursor.fetchall()
        
        for perfil_data in perfis:
            user_id, profile_picture, bio, phone, birth_date, created_at, updated_at = perfil_data
            
            try:
                user = User.objects.get(id=user_id)
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'profile_picture': profile_picture if profile_picture else None,
                        'bio': bio or '',
                        'phone': phone or '',
                        'birth_date': birth_date,
                    }
                )
                if created:
                    print(f"  ✅ Perfil do usuário {user.username} migrado")
                else:
                    print(f"  ⏭️ Perfil do usuário {user.username} já existe, pulando...")
            except Exception as e:
                print(f"  ❌ Erro ao migrar perfil do usuário {user_id}: {e}")
        
        # 5. Migrar feedbacks
        print("💬 Migrando feedbacks...")
        cursor.execute("""
            SELECT user_id, aparelho_id, rating, comment, created_at
            FROM aparelhos_feedback
        """)
        feedbacks = cursor.fetchall()
        
        for feedback_data in feedbacks:
            user_id, aparelho_id, rating, comment, created_at = feedback_data
            
            try:
                user = User.objects.get(id=user_id)
                aparelho = Aparelho.objects.get(id=aparelho_id)
                
                feedback = Feedback.objects.create(
                    user=user,
                    aparelho=aparelho,
                    rating=rating or 0,
                    comment=comment or '',
                    created_at=created_at
                )
                print(f"  ✅ Feedback do usuário {user.username} para {aparelho.exercise_name} migrado")
            except Exception as e:
                print(f"  ❌ Erro ao migrar feedback: {e}")
        
        # 6. Migrar visualizações
        print("👁️ Migrando visualizações...")
        cursor.execute("""
            SELECT user_id, aparelho_id, count, last_clicked, viewed_at, updated_at
            FROM aparelhos_visualizacao
        """)
        visualizacoes = cursor.fetchall()
        
        for viz_data in visualizacoes:
            user_id, aparelho_id, count, last_clicked, viewed_at, updated_at = viz_data
            
            try:
                user = User.objects.get(id=user_id)
                aparelho = Aparelho.objects.get(id=aparelho_id)
                
                visualizacao = Visualizacao.objects.create(
                    user=user,
                    aparelho=aparelho,
                    count=count or 0,
                    last_clicked=last_clicked,
                    viewed_at=viewed_at,
                    updated_at=updated_at
                )
                print(f"  ✅ Visualização do usuário {user.username} para {aparelho.exercise_name} migrada")
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
