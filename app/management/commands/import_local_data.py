from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
import shutil

class Command(BaseCommand):
    help = 'Importa dados do banco local para o Render'

    def handle(self, *args, **options):
        self.stdout.write('📊 Importando dados do banco local...')
        
        # Caminho do banco local
        local_db = 'db.sqlite3'
        
        if os.path.exists(local_db):
            try:
                # Fazer backup do banco atual
                if os.path.exists('db_backup.sqlite3'):
                    os.remove('db_backup.sqlite3')
                
                # Copiar banco local para o Render
                shutil.copy2(local_db, 'db_backup.sqlite3')
                
                self.stdout.write('✅ Banco local copiado com sucesso!')
                self.stdout.write('📝 Dados importados:')
                
                # Verificar dados importados
                from django.contrib.auth.models import User
                from aparelhos.models import Aparelho
                
                user_count = User.objects.count()
                aparelho_count = Aparelho.objects.count()
                
                self.stdout.write(f'👥 Usuários: {user_count}')
                self.stdout.write(f'🏋️ Aparelhos: {aparelho_count}')
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Erro ao importar: {e}'))
        else:
            self.stdout.write(self.style.ERROR('❌ Banco local não encontrado!'))
