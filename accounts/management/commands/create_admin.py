from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Cria ou atualiza o usuário administrador'

    def handle(self, *args, **options):
        # Dados do administrador
        admin_username = 'WeslleyDev'
        admin_email = 'weslleydevpereira@gmail.com'
        admin_password = 'WeslleyDev@dmin123'
        
        try:
            # Verificar se o usuário já existe
            user = User.objects.get(username=admin_username)
            
            # Atualizar dados do usuário existente
            user.email = admin_email
            user.set_password(admin_password)
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Usuário administrador "{admin_username}" atualizado com sucesso!')
            )
            
        except ObjectDoesNotExist:
            # Criar novo usuário administrador
            user = User.objects.create_user(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                is_superuser=True,
                is_staff=True,
                is_active=True
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Usuário administrador "{admin_username}" criado com sucesso!')
            )
        
        # Remover outros usuários com permissões de administrador
        other_admins = User.objects.filter(
            is_superuser=True
        ).exclude(username=admin_username)
        
        if other_admins.exists():
            for admin in other_admins:
                admin.is_superuser = False
                admin.is_staff = False
                admin.save()
                self.stdout.write(
                    self.style.WARNING(f'Permissões administrativas removidas do usuário "{admin.username}"')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Configuração do administrador concluída!')
        )


