from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core import serializers
import os
import json
from datetime import datetime

class Command(BaseCommand):
    help = 'Faz backup dos dados atuais'

    def handle(self, *args, **options):
        self.stdout.write('💾 Iniciando backup dos dados...')
        
        try:
            # Criar nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f'backup_data_{timestamp}.json'
            
            # Fazer backup de todos os dados
            call_command('dumpdata', 
                        'auth.user', 
                        'accounts.userprofile', 
                        'aparelhos.aparelho',
                        'aparelhos.grupo_muscular',
                        'aparelhos.feedback',
                        'aparelhos.visualizacao',
                        '--indent', '2',
                        '--output', backup_file)
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Backup criado: {backup_file}')
            )
            
            # Também atualizar o arquivo principal de backup
            call_command('dumpdata', 
                        'auth.user', 
                        'accounts.userprofile', 
                        'aparelhos.aparelho',
                        'aparelhos.grupo_muscular',
                        'aparelhos.feedback',
                        'aparelhos.visualizacao',
                        '--indent', '2',
                        '--output', 'backup_data.json')
            
            self.stdout.write(
                self.style.SUCCESS('✅ Backup principal atualizado: backup_data.json')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro ao fazer backup: {e}')
            )
