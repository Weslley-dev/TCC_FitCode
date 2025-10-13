from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Restaura dados do backup'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='backup_data.json',
            help='Arquivo de backup para restaurar'
        )

    def handle(self, *args, **options):
        backup_file = options['file']
        
        self.stdout.write(f'🔄 Restaurando dados de {backup_file}...')
        
        # Verificar se o arquivo existe
        if not os.path.exists(backup_file):
            self.stdout.write(
                self.style.ERROR(f'❌ Arquivo {backup_file} não encontrado!')
            )
            return
        
        try:
            # Limpar dados existentes (opcional)
            self.stdout.write('🧹 Limpando dados existentes...')
            call_command('flush', '--noinput')
            
            # Restaurar dados
            call_command('loaddata', backup_file)
            
            self.stdout.write(
                self.style.SUCCESS('✅ Dados restaurados com sucesso!')
            )
            
            # Verificar dados restaurados
            from django.contrib.auth.models import User
            from aparelhos.models import Aparelho, Feedback, Visualizacao
            from accounts.models import UserProfile
            
            self.stdout.write(f'📊 Dados restaurados:')
            self.stdout.write(f'  👥 Usuários: {User.objects.count()}')
            self.stdout.write(f'  🏋️ Aparelhos: {Aparelho.objects.count()}')
            self.stdout.write(f'  💬 Feedbacks: {Feedback.objects.count()}')
            self.stdout.write(f'  👁️ Visualizações: {Visualizacao.objects.count()}')
            self.stdout.write(f'  👤 Perfis: {UserProfile.objects.count()}')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao restaurar dados: {e}')
            )
