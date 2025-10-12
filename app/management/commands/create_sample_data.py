from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from aparelhos.models import Aparelho, GrupoMuscular
from accounts.models import UserProfile
from django.utils import timezone
import os

class Command(BaseCommand):
    help = 'Cria dados de exemplo para o Render'

    def handle(self, *args, **options):
        self.stdout.write('🏋️ Criando dados de exemplo...')
        
        # Criar grupos musculares
        grupos = [
            {'nome': 'Peito', 'descricao': 'Exercícios para o peitoral'},
            {'nome': 'Costas', 'descricao': 'Exercícios para as costas'},
            {'nome': 'Pernas', 'descricao': 'Exercícios para as pernas'},
            {'nome': 'Braços', 'descricao': 'Exercícios para os braços'},
            {'nome': 'Ombros', 'descricao': 'Exercícios para os ombros'},
        ]
        
        for grupo_data in grupos:
            grupo, created = GrupoMuscular.objects.get_or_create(
                nome=grupo_data['nome'],
                defaults={'descricao': grupo_data['descricao']}
            )
            if created:
                self.stdout.write(f'✅ Grupo criado: {grupo.nome}')
        
        # Criar aparelhos de exemplo
        aparelhos_data = [
            {
                'nome': 'Supino Reto',
                'descricao': 'Exercício para desenvolvimento do peitoral',
                'instrucoes': 'Deite no banco, segure a barra com pegada média e desça até o peito',
                'grupo_muscular': 'Peito',
                'dificuldade': 'Intermediário',
                'series': 3,
                'repeticoes': '8-12'
            },
            {
                'nome': 'Puxada Frontal',
                'descricao': 'Exercício para desenvolvimento das costas',
                'instrucoes': 'Sente na máquina, puxe a barra até o peito',
                'grupo_muscular': 'Costas',
                'dificuldade': 'Iniciante',
                'series': 3,
                'repeticoes': '10-15'
            },
            {
                'nome': 'Leg Press',
                'descricao': 'Exercício para desenvolvimento das pernas',
                'instrucoes': 'Sente na máquina, empurre o peso com as pernas',
                'grupo_muscular': 'Pernas',
                'dificuldade': 'Iniciante',
                'series': 4,
                'repeticoes': '12-15'
            },
            {
                'nome': 'Rosca Bíceps',
                'descricao': 'Exercício para desenvolvimento do bíceps',
                'instrucoes': 'Segure os halteres, flexione os braços',
                'grupo_muscular': 'Braços',
                'dificuldade': 'Iniciante',
                'series': 3,
                'repeticoes': '10-12'
            },
            {
                'nome': 'Desenvolvimento',
                'descricao': 'Exercício para desenvolvimento dos ombros',
                'instrucoes': 'Sente no banco, empurre os halteres para cima',
                'grupo_muscular': 'Ombros',
                'dificuldade': 'Intermediário',
                'series': 3,
                'repeticoes': '8-10'
            }
        ]
        
        for aparelho_data in grupos:
            grupo = GrupoMuscular.objects.get(nome=aparelho_data['grupo_muscular'])
            aparelho, created = Aparelho.objects.get_or_create(
                nome=aparelho_data['nome'],
                defaults={
                    'descricao': aparelho_data['descricao'],
                    'instrucoes': aparelho_data['instrucoes'],
                    'grupo_muscular': grupo,
                    'dificuldade': aparelho_data['dificuldade'],
                    'series': aparelho_data['series'],
                    'repeticoes': aparelho_data['repeticoes']
                }
            )
            if created:
                self.stdout.write(f'✅ Aparelho criado: {aparelho.nome}')
        
        # Criar usuário de exemplo
        if not User.objects.filter(username='usuario_teste').exists():
            user = User.objects.create_user(
                username='usuario_teste',
                email='teste@example.com',
                password='123456',
                first_name='Usuário',
                last_name='Teste'
            )
            self.stdout.write('✅ Usuário de teste criado: usuario_teste / 123456')
        
        # Estatísticas finais
        user_count = User.objects.count()
        aparelho_count = Aparelho.objects.count()
        grupo_count = GrupoMuscular.objects.count()
        
        self.stdout.write('📊 Dados criados:')
        self.stdout.write(f'👥 Usuários: {user_count}')
        self.stdout.write(f'🏋️ Aparelhos: {aparelho_count}')
        self.stdout.write(f'💪 Grupos musculares: {grupo_count}')
        
        self.stdout.write(self.style.SUCCESS('🎉 Dados de exemplo criados com sucesso!'))
