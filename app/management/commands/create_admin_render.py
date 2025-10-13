from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria usuário administrador no Render'

    def handle(self, *args, **options):
        self.stdout.write('🚨 CRIANDO ADMINISTRADOR NO RENDER...')
        
        # Deletar todos os superusuários existentes
        User.objects.filter(is_superuser=True).delete()
        self.stdout.write('🧹 Usuários administradores existentes removidos')
        
        # Criar novo administrador
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@fitcode.com',
            password='admin123',
            first_name='Admin',
            last_name='FitCode'
        )
        
        self.stdout.write(
            self.style.SUCCESS('✅ Administrador criado com sucesso!')
        )
        self.stdout.write(f'👤 Username: {admin.username}')
        self.stdout.write(f'📧 Email: {admin.email}')
        self.stdout.write(f'🔑 Senha: admin123')
        self.stdout.write(f'✅ Ativo: {admin.is_active}')
        self.stdout.write(f'🔧 Superuser: {admin.is_superuser}')
        self.stdout.write(f'👨‍💼 Staff: {admin.is_staff}')
        
        # Testar login
        from django.contrib.auth import authenticate
        user = authenticate(username='admin', password='admin123')
        if user:
            self.stdout.write(
                self.style.SUCCESS('✅ Login testado com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Erro no login!')
            )
        
        self.stdout.write('\n🌐 ACESSO:')
        self.stdout.write('URL: https://tcc-fitcode-web.onrender.com/admin/login/')
        self.stdout.write('Usuário: admin')
        self.stdout.write('Senha: admin123')
