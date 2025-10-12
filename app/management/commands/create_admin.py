from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria ou atualiza o usuário administrador'

    def handle(self, *args, **options):
        self.stdout.write('👤 Configurando usuário administrador...')
        
        try:
            # Deletar usuário existente se houver
            if User.objects.filter(username='WeslleyDev').exists():
                User.objects.filter(username='WeslleyDev').delete()
                self.stdout.write('🗑️ Usuário existente removido')
            
            # Criar novo usuário
            user = User.objects.create_user(
                username='WeslleyDev',
                email='weslleydevpereira@gmail.com',
                password='WeslleyDev@dmin123',
                first_name='Weslley',
                last_name='Developer',
                is_superuser=True,
                is_staff=True,
                is_active=True
            )
            
            self.stdout.write('✅ Usuário administrador criado!')
            
            # Verificar se foi criado corretamente
            user_check = User.objects.get(username='WeslleyDev')
            self.stdout.write('📋 Dados do administrador:')
            self.stdout.write(f'   👤 Usuário: {user_check.username}')
            self.stdout.write(f'   📧 E-mail: {user_check.email}')
            self.stdout.write(f'   🔑 Senha: WeslleyDev@dmin123')
            self.stdout.write(f'   🔐 Superusuário: {user_check.is_superuser}')
            self.stdout.write(f'   👨‍💼 Staff: {user_check.is_staff}')
            self.stdout.write(f'   ✅ Ativo: {user_check.is_active}')
            
            # Testar login
            from django.contrib.auth import authenticate
            auth_user = authenticate(username='WeslleyDev', password='WeslleyDev@dmin123')
            if auth_user:
                self.stdout.write('✅ Login testado com sucesso!')
            else:
                self.stdout.write('❌ Erro no teste de login!')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro ao criar administrador: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
