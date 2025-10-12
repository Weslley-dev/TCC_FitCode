from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Força a criação do usuário administrador'

    def handle(self, *args, **options):
        self.stdout.write('🔨 Forçando criação do usuário administrador...')
        
        try:
            # Deletar TODOS os usuários WeslleyDev
            User.objects.filter(username='WeslleyDev').delete()
            self.stdout.write('🗑️ Usuários existentes removidos')
            
            # Criar usuário do zero
            user = User.objects.create_user(
                username='WeslleyDev',
                email='weslleydevpereira@gmail.com',
                password='WeslleyDev@dmin123',
                first_name='Weslley',
                last_name='Developer'
            )
            
            # Definir permissões
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            
            self.stdout.write('✅ Usuário criado com sucesso!')
            
            # Verificar criação
            created_user = User.objects.get(username='WeslleyDev')
            self.stdout.write(f'👤 Usuário: {created_user.username}')
            self.stdout.write(f'📧 E-mail: {created_user.email}')
            self.stdout.write(f'🔐 Superusuário: {created_user.is_superuser}')
            self.stdout.write(f'👨‍💼 Staff: {created_user.is_staff}')
            self.stdout.write(f'✅ Ativo: {created_user.is_active}')
            
            # Testar autenticação
            from django.contrib.auth import authenticate
            auth_user = authenticate(username='WeslleyDev', password='WeslleyDev@dmin123')
            if auth_user:
                self.stdout.write('🎉 LOGIN FUNCIONANDO!')
            else:
                self.stdout.write('❌ LOGIN FALHOU!')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro: {e}')
            import traceback
            self.stdout.write(traceback.format_exc())
