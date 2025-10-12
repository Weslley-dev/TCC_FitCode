from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Inicializa o banco de dados no Render.com'

    def handle(self, *args, **options):
        try:
            # Executar migrações
            self.stdout.write('Executando migrações...')
            call_command('migrate', verbosity=2)
            
            # Verificar se as tabelas foram criadas
            user_count = User.objects.count()
            self.stdout.write(f'Usuários no banco: {user_count}')
            
            # Coletar arquivos estáticos
            self.stdout.write('Coletando arquivos estáticos...')
            call_command('collectstatic', '--noinput', verbosity=0)
            
            self.stdout.write(self.style.SUCCESS('Configuração concluída com sucesso!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro na configuração: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
