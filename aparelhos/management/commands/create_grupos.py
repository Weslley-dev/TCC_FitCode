from django.core.management.base import BaseCommand
from aparelhos.models import Grupo_muscular

class Command(BaseCommand):
    help = 'Cria todos os grupos musculares'

    def handle(self, *args, **options):
        grupos = [
            'Perna',
            'Panturrilhas', 
            'Ombros',
            'Costas',
            'Peito',
            'Bíceps',
            'Tríceps',
            'Antebraço',
            'Abdômen',
            'Glúteos',
            'Posterior de Coxa',
            'Quadríceps',
            'Trapézio',
            'Dorsal',
            'Lombar'
        ]
        
        created_count = 0
        for grupo in grupos:
            grupo_obj, created = Grupo_muscular.objects.get_or_create(name=grupo)
            if created:
                created_count += 1
                self.stdout.write(f'✅ Criado: {grupo}')
            else:
                self.stdout.write(f'⚠️ Já existe: {grupo}')
        
        self.stdout.write(
            self.style.SUCCESS(f'🎉 Processo concluído! {created_count} grupos criados.')
        )
