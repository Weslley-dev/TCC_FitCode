from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria ou atualiza o usuário administrador'

    def handle(self, *args, **options):
        self.stdout.write('👤 Configurando usuário administrador...')
        
        try:
            # Verificar se usuário já existe
            if User.objects.filter(username='WeslleyDev').exists():
                # Atualizar usuário existente
                user = User.objects.get(username='WeslleyDev')
                user.set_password('WeslleyDev@dmin123')
                user.email = 'weslleydevpereira@gmail.com'
                user.first_name = 'Weslley'
                user.last_name = 'Developer'
                user.is_superuser = True
                user.is_staff = True
                user.is_active = True
                user.save()
                self.stdout.write('✅ Usuário administrador atualizado!')
            else:
                # Criar novo usuário
                user = User.objects.create_superuser(
                    username='WeslleyDev',
                    email='weslleydevpereira@gmail.com',
                    password='WeslleyDev@dmin123',
                    first_name='Weslley',
                    last_name='Developer'
                )
                self.stdout.write('✅ Usuário administrador criado!')
            
            self.stdout.write('📋 Dados do administrador:')
            self.stdout.write(f'   👤 Usuário: WeslleyDev')
            self.stdout.write(f'   📧 E-mail: weslleydevpereira@gmail.com')
            self.stdout.write(f'   🔑 Senha: WeslleyDev@dmin123')
            self.stdout.write(f'   🔐 Superusuário: {user.is_superuser}')
            self.stdout.write(f'   👨‍💼 Staff: {user.is_staff}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro ao criar administrador: {e}'))
