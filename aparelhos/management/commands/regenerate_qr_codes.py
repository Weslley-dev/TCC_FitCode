from django.core.management.base import BaseCommand
from aparelhos.models import Aparelho

class Command(BaseCommand):
    help = 'Regenera todos os QR Codes existentes com a nova URL'

    def handle(self, *args, **options):
        aparelhos = Aparelho.objects.all()
        count = 0
        
        for aparelho in aparelhos:
            # Remove o QR Code existente se houver
            if aparelho.qr_code:
                aparelho.qr_code.delete(save=False)
                aparelho.qr_code = None
            
            # Gera novo QR Code
            aparelho.generate_qr_code()
            aparelho.save()
            count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'QR Code regenerado para: {aparelho.exercise_name}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Total de QR Codes regenerados: {count}')
        )
