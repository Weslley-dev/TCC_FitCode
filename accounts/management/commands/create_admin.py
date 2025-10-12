from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria um superusuário para o Railway'

    def handle(self, *args, **options):
        # Verificar se já existe
        if User.objects.filter(username='WeslleyDev').exists():
            self.stdout.write(
                self.style.ERROR('❌ Usuário "WeslleyDev" já existe!')
            )
            return

        # Criar superusuário
        user = User.objects.create_superuser(
            username='WeslleyDev',
            email='weslleydevpereira@gmail.com',
            password='WeslleyDev@dmin123'
        )

        self.stdout.write(
            self.style.SUCCESS('✅ Superusuário criado com sucesso!')
        )
        self.stdout.write(f'👤 Username: {user.username}')
        self.stdout.write(f'📧 Email: {user.email}')
        self.stdout.write(f'🔑 Senha: WeslleyDev@dmin123')
        self.stdout.write('')
        self.stdout.write('🌐 Acesse o admin em: https://tccfitcode-production.up.railway.app/admin/')