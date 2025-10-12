from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria usuário administrador de forma simples'

    def handle(self, *args, **options):
        # Deletar se existir
        User.objects.filter(username='WeslleyDev').delete()
        
        # Criar novo
        user = User.objects.create_user(
            username='WeslleyDev',
            email='weslleydevpereira@gmail.com',
            password='WeslleyDev@dmin123'
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        
        print('✅ Usuário criado: WeslleyDev / WeslleyDev@dmin123')
