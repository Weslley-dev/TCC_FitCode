from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Importa dados do SQLite para PostgreSQL no Railway'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Iniciando importação de dados...')
        
        # Verificar se o arquivo existe
        if not os.path.exists('railway_admin_data.json'):
            self.stdout.write(
                self.style.ERROR('❌ Arquivo railway_admin_data.json não encontrado!')
            )
            return
        
        try:
            # Importar dados
            call_command('loaddata', 'railway_admin_data.json')
            self.stdout.write(
                self.style.SUCCESS('✅ Dados importados com sucesso!')
            )
            self.stdout.write('👤 Superusuário: WeslleyDev')
            self.stdout.write('📧 Email: weslleydevpereira@gmail.com')
            self.stdout.write('🔑 Senha: WeslleyDev@dmin123')
            self.stdout.write('🌐 Admin: https://tccfitcode-production.up.railway.app/admin/')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao importar dados: {e}')
            )
