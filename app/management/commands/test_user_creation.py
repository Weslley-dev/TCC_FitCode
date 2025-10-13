from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Teste simples de criação de usuário'

    def handle(self, *args, **options):
        self.stdout.write('🧪 Testando criação de usuário...')

        try:
            # Verificar usuários existentes
            users = User.objects.all()
            self.stdout.write(f'👥 Usuários existentes: {users.count()}')
            
            for user in users:
                self.stdout.write(f'  - {user.username} (superuser: {user.is_superuser}, staff: {user.is_staff})')

            # Criar usuário de teste
            if not User.objects.filter(username='WeslleyTcc').exists():
                self.stdout.write('🔄 Criando usuário WeslleyTcc...')
                user = User.objects.create_user(
                    username='WeslleyTcc',
                    email='weslleypereira307@gmail.com',
                    password='FitCode2024!',
                    first_name='Weslley',
                    last_name='TCC',
                    is_superuser=True,
                    is_staff=True,
                    is_active=True
                )
                self.stdout.write('✅ Usuário criado!')
            else:
                self.stdout.write('⚠️ Usuário já existe, atualizando...')
                user = User.objects.get(username='WeslleyTcc')
                user.set_password('FitCode2024!')
                user.is_superuser = True
                user.is_staff = True
                user.is_active = True
                user.save()
                self.stdout.write('✅ Usuário atualizado!')

            # Verificar se funcionou
            user_check = User.objects.get(username='WeslleyTcc')
            self.stdout.write('📋 Dados finais:')
            self.stdout.write(f'  👤 Usuário: {user_check.username}')
            self.stdout.write(f'  🔐 Superusuário: {user_check.is_superuser}')
            self.stdout.write(f'  👨‍💼 Staff: {user_check.is_staff}')
            self.stdout.write(f'  ✅ Ativo: {user_check.is_active}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
