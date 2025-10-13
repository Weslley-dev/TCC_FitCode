from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria superusuário para o Render'

    def handle(self, *args, **options):
        self.stdout.write('👤 Criando superusuário WeslleyTcc...')

        try:
            # Verificar se já existe
            if User.objects.filter(username='WeslleyTcc').exists():
                self.stdout.write('⚠️ Usuário WeslleyTcc já existe. Atualizando...')
                user = User.objects.get(username='WeslleyTcc')
                user.set_password('fitcode@dmin1020')
                user.email = 'weslleypereira307@gmail.com'
                user.is_superuser = True
                user.is_staff = True
                user.is_active = True
                user.save()
                self.stdout.write('✅ Usuário WeslleyTcc atualizado!')
            else:
                # Criar novo usuário
                user = User.objects.create_user(
                    username='WeslleyTcc',
                    email='weslleypereira307@gmail.com',
                    password='fitcode@dmin1020',
                    first_name='Weslley',
                    last_name='TCC',
                    is_superuser=True,
                    is_staff=True,
                    is_active=True
                )
                self.stdout.write('✅ Usuário WeslleyTcc criado!')

            # Verificar dados
            user_check = User.objects.get(username='WeslleyTcc')
            self.stdout.write('📋 Dados do superusuário:')
            self.stdout.write(f'   👤 Usuário: {user_check.username}')
            self.stdout.write(f'   📧 E-mail: {user_check.email}')
            self.stdout.write(f'   🔑 Senha: fitcode@dmin1020')
            self.stdout.write(f'   🔐 Superusuário: {user_check.is_superuser}')
            self.stdout.write(f'   👨‍💼 Staff: {user_check.is_staff}')
            self.stdout.write(f'   ✅ Ativo: {user_check.is_active}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro ao criar superusuário: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
