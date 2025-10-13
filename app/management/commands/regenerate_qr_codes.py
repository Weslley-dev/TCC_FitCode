from django.core.management.base import BaseCommand
from aparelhos.models import Aparelho

class Command(BaseCommand):
    help = 'Regenera todos os QR codes dos exercícios'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Regenerando QR codes...')
        
        aparelhos = Aparelho.objects.all()
        total = aparelhos.count()
        
        if total == 0:
            self.stdout.write('❌ Nenhum exercício encontrado!')
            return
        
        self.stdout.write(f'📊 Encontrados {total} exercícios')
        
        regenerated = 0
        for aparelho in aparelhos:
            try:
                # Forçar regeneração do QR code
                aparelho.qr_code.delete(save=False)  # Deletar QR code existente
                aparelho.qr_code = None
                aparelho.save()  # Isso vai gerar um novo QR code
                
                regenerated += 1
                self.stdout.write(f'✅ QR code regenerado: {aparelho.exercise_name}')
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erro ao regenerar QR code de {aparelho.exercise_name}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'🎉 Regeneração concluída! {regenerated}/{total} QR codes regenerados')
        )
        
        # Mostrar URLs dos QR codes
        self.stdout.write('\n🔗 URLs dos QR codes:')
        for aparelho in aparelhos:
            if aparelho.qr_code:
                from django.conf import settings
                base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
                qr_url = f"{base_url}/aparelhos/qr/{aparelho.id}/"
                self.stdout.write(f'  - {aparelho.exercise_name}: {qr_url}')
