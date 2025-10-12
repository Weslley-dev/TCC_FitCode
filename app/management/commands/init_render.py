from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Inicializa o banco de dados no Render.com'

    def handle(self, *args, **options):
        try:
            # Executar migrações
            self.stdout.write('Executando migrações...')
            call_command('migrate', verbosity=0)
            
            # Coletar arquivos estáticos
            self.stdout.write('Coletando arquivos estáticos...')
            call_command('collectstatic', '--noinput', verbosity=0)
            
            self.stdout.write(self.style.SUCCESS('Configuração concluída com sucesso!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro na configuração: {e}'))
