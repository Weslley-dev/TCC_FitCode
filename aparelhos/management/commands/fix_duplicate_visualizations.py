from django.core.management.base import BaseCommand
from aparelhos.models import Visualizacao
from django.db.models import Count

class Command(BaseCommand):
    help = 'Corrige visualizações duplicadas no banco de dados'

    def handle(self, *args, **options):
        # Encontrar visualizações duplicadas
        duplicates = Visualizacao.objects.values('user', 'aparelho').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        total_fixed = 0
        
        for duplicate in duplicates:
            user_id = duplicate['user']
            aparelho_id = duplicate['aparelho']
            
            # Buscar todas as visualizações duplicadas
            visualizacoes = Visualizacao.objects.filter(
                user_id=user_id,
                aparelho_id=aparelho_id
            ).order_by('viewed_at')
            
            if visualizacoes.count() > 1:
                # Manter a primeira e somar os counts das outras
                first_viz = visualizacoes.first()
                total_count = sum(viz.count for viz in visualizacoes)
                
                # Atualizar a primeira com o total
                first_viz.count = total_count
                first_viz.save()
                
                # Deletar as duplicatas
                visualizacoes.exclude(id=first_viz.id).delete()
                
                total_fixed += visualizacoes.count() - 1
                
                self.stdout.write(
                    f'Corrigido: Usuário {user_id}, Aparelho {aparelho_id} - '
                    f'Count total: {total_count}'
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Correção concluída! {total_fixed} visualizações duplicadas foram corrigidas.')
        )
