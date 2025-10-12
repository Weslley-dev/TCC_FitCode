from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Força importação de dados no Railway'

    def handle(self, *args, **options):
        self.stdout.write('🚀 FORÇANDO IMPORTAÇÃO DE DADOS...')
        
        # Verificar se já existe
        if User.objects.filter(username='WeslleyDev').exists():
            self.stdout.write('✅ Superusuário já existe!')
        else:
            self.stdout.write('📤 Importando dados...')
            try:
                call_command('loaddata', 'railway_admin_data.json')
                self.stdout.write(
                    self.style.SUCCESS('✅ DADOS IMPORTADOS COM SUCESSO!')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erro: {e}')
                )
                return
        
        # Verificar dados
        user_count = User.objects.count()
        self.stdout.write(f'👥 Total de usuários: {user_count}')
        
        # Verificar aparelhos
        try:
            from aparelhos.models import Aparelho
            aparelho_count = Aparelho.objects.count()
            self.stdout.write(f'🏋️ Total de aparelhos: {aparelho_count}')
        except Exception as e:
            self.stdout.write(f'❌ Erro ao verificar aparelhos: {e}')
        
        self.stdout.write('🌐 Acesse: https://tccfitcode-production.up.railway.app/admin/')
        self.stdout.write('👤 Username: WeslleyDev')
        self.stdout.write('🔑 Senha: WeslleyDev@dmin123')
