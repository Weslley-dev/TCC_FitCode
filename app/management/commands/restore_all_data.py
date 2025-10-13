from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Restaura todos os dados no Render'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Restaurando todos os dados no Render...')
        
        # Lista de arquivos de backup para tentar
        backup_files = [
            'dados_completos.json',
            'backup_data_atual.json',
            'backup_data.json',
            'render_data.json',
            'admin_data.json'
        ]
        
        restored = False
        for backup_file in backup_files:
            if os.path.exists(backup_file):
                self.stdout.write(f'🔄 Tentando restaurar de {backup_file}...')
                try:
                    # Limpar dados existentes primeiro
                    self.stdout.write('🧹 Limpando dados existentes...')
                    call_command('flush', '--noinput')
                    
                    # Restaurar dados
                    call_command('loaddata', backup_file)
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Dados restaurados de {backup_file}!')
                    )
                    restored = True
                    break
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Erro ao restaurar {backup_file}: {e}')
                    )
                    continue
        
        if not restored:
            self.stdout.write(
                self.style.ERROR('❌ Nenhum arquivo de backup encontrado!')
            )
            return
        
        # Verificar dados restaurados
        from django.contrib.auth.models import User
        from aparelhos.models import Aparelho, Feedback, Visualizacao, Grupo_muscular
        from accounts.models import UserProfile
        
        self.stdout.write('\n📊 Dados restaurados:')
        self.stdout.write(f'  👥 Usuários: {User.objects.count()}')
        self.stdout.write(f'  🏋️ Aparelhos: {Aparelho.objects.count()}')
        self.stdout.write(f'  💪 Grupos musculares: {Grupo_muscular.objects.count()}')
        self.stdout.write(f'  💬 Feedbacks: {Feedback.objects.count()}')
        self.stdout.write(f'  👁️ Visualizações: {Visualizacao.objects.count()}')
        self.stdout.write(f'  👤 Perfis: {UserProfile.objects.count()}')
        
        # Listar alguns aparelhos
        aparelhos = Aparelho.objects.all()[:5]
        if aparelhos:
            self.stdout.write('\n🏋️ Aparelhos encontrados:')
            for aparelho in aparelhos:
                self.stdout.write(f'  - {aparelho.exercise_name}')
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 Restauração concluída com sucesso!')
        )
