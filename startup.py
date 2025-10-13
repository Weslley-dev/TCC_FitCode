#!/usr/bin/env python
"""
Script de inicialização para Render.com
Executa migrações e cria dados iniciais
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    django.setup()
    
    print("🚀 Iniciando configuração do Render...")
    
    # Executar migrações
    print("📊 Executando migrações...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        print("✅ Migrações executadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro nas migrações: {e}")
        sys.exit(1)
    
    # Verificar se as tabelas foram criadas
    try:
        user_count = User.objects.count()
        print(f"👥 Usuários no banco: {user_count}")
    except Exception as e:
        print(f"❌ Erro ao verificar banco: {e}")
        sys.exit(1)
    
    # Carregar dados do backup se não existirem usuários
    print("📦 Verificando dados...")
    try:
        from django.contrib.auth.models import User
        user_count = User.objects.count()
        print(f"👥 Usuários encontrados: {user_count}")
        
        if user_count == 0:
            print("🔄 Nenhum usuário encontrado, carregando dados do backup...")
            
            # Verificar se o arquivo existe
            import os
            if os.path.exists('render_data.json'):
                print("✅ Arquivo render_data.json encontrado")
                execute_from_command_line(['manage.py', 'loaddata', 'render_data.json'])
                print("✅ Dados carregados com sucesso!")
                
                # Verificar se os dados foram carregados
                new_user_count = User.objects.count()
                print(f"👥 Usuários após carregamento: {new_user_count}")
            else:
                print("❌ Arquivo render_data.json não encontrado")
                print("📁 Arquivos no diretório:")
                for file in os.listdir('.'):
                    print(f"  - {file}")
        else:
            print("✅ Dados já existem, pulando carregamento")
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        import traceback
        print(traceback.format_exc())

    # Criar/atualizar superusuário
    print("👤 Configurando usuário administrador...")
    try:
        execute_from_command_line(['manage.py', 'force_create_admin'])
        print("✅ Administrador configurado!")
    except Exception as e:
        print(f"❌ Erro ao configurar administrador: {e}")
    
    # Criar dados de exemplo se não existirem
    from aparelhos.models import Aparelho
    if Aparelho.objects.count() == 0:
        print("🏋️ Criando dados de exemplo...")
        try:
            execute_from_command_line(['manage.py', 'create_sample_data'])
            print("✅ Dados de exemplo criados!")
        except Exception as e:
            print(f"❌ Erro ao criar dados de exemplo: {e}")
    
    # Coletar arquivos estáticos
    print("📁 Coletando arquivos estáticos...")
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Arquivos estáticos coletados!")
    except Exception as e:
        print(f"❌ Erro ao coletar estáticos: {e}")
    
    print("🎉 Configuração concluída com sucesso!")
