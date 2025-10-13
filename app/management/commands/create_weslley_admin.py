from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria superuser WeslleyDev no Render'

    def handle(self, *args, **options):
        self.stdout.write('🚨 CRIANDO SUPERUSER WESLLEYDEV...')
        
        # Deletar usuário existente se houver
        User.objects.filter(username='WeslleyDev').delete()
        self.stdout.write('🧹 Usuário WeslleyDev existente removido')
        
        # Criar novo superuser
        user = User.objects.create_superuser(
            username='WeslleyDev',
            email='weslleydevpereira@gmail.com',
            password='WeslleyDev@dmin123',
            first_name='Weslley',
            last_name='Dev'
        )
        
        self.stdout.write(
            self.style.SUCCESS('✅ Superuser WeslleyDev criado com sucesso!')
        )
        self.stdout.write(f'👤 Username: {user.username}')
        self.stdout.write(f'📧 Email: {user.email}')
        self.stdout.write(f'🔑 Senha: WeslleyDev@dmin123')
        self.stdout.write(f'✅ Ativo: {user.is_active}')
        self.stdout.write(f'🔧 Superuser: {user.is_superuser}')
        self.stdout.write(f'👨‍💼 Staff: {user.is_staff}')
        
        # Testar login
        from django.contrib.auth import authenticate
        test_user = authenticate(username='WeslleyDev', password='WeslleyDev@dmin123')
        if test_user:
            self.stdout.write(
                self.style.SUCCESS('✅ Login testado com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Erro no login!')
            )
        
        self.stdout.write('\n🌐 ACESSO:')
        self.stdout.write('URL: https://tcc-fitcode-web.onrender.com/admin/login/')
        self.stdout.write('Usuário: WeslleyDev')
        self.stdout.write('Senha: WeslleyDev@dmin123')
