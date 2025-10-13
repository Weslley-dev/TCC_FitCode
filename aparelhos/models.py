from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

class Grupo_muscular(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Grupo Muscular"
        verbose_name_plural = "Grupos Musculares"

    def __str__(self):
        return self.name

class Aparelho(models.Model):
    id = models.AutoField(primary_key=True)
    exercise_name = models.CharField("Nome do Exercício", max_length=200, blank=True, null=True)
    grupo_muscular = models.ForeignKey(
        Grupo_muscular,
        on_delete=models.PROTECT,
        related_name='aparelhos',
        null=True,      
        blank=True
    )
    video = models.FileField(upload_to='aparelhos/videos/', blank=True, null=True)
    image = models.ImageField(upload_to='aparelhos/', blank=True, null=True)  
    instructions = models.TextField("Instruções de Execução", blank=True)
    qr_code = models.ImageField(upload_to='aparelhos/qrcodes/', blank=True, null=True, help_text="QR Code gerado automaticamente")

    class Meta:
        ordering = ["exercise_name"]

    def __str__(self):
        return self.exercise_name or "Sem nome"
    
    def generate_qr_code(self):
        """Gera QR Code para o exercício"""
        if not self.exercise_name:
            print(f"⚠️ Aparelho {self.id} sem nome, pulando geração de QR")
            return
        
        try:
            import qrcode
            import io
            from django.core.files.base import ContentFile
        except ImportError as e:
            print(f"❌ Erro ao importar bibliotecas: {e}")
            return
        
        # URL que será codificada no QR Code
        from django.conf import settings
        base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
        qr_data = f"{base_url}/aparelhos/qr/{self.id}/"
        print(f"🔗 Gerando QR para: {qr_data}")
        
        try:
            # Criar QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Criar imagem
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Converter para bytes
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Salvar no campo qr_code
            filename = f"qr_{self.id}_{self.exercise_name.replace(' ', '_')}.png"
            self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
            print(f"✅ QR code gerado: {filename}")
            
        except Exception as e:
            print(f"❌ Erro ao gerar QR code: {e}")
            import traceback
            traceback.print_exc()
    
    def save(self, *args, **kwargs):
        # Gerar QR Code antes de salvar
        super().save(*args, **kwargs)
        if not self.qr_code:  # Só gera se não existir
            self.generate_qr_code()
            super().save(*args, **kwargs)  # Salva novamente com o QR Code

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    aparelho = models.ForeignKey(Aparelho, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], help_text="Avaliação de 1 a 5 estrelas")
    comment = models.TextField("Comentário", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
        unique_together = ['user', 'aparelho']  # Um usuário só pode dar feedback uma vez por exercício
    
    def __str__(self):
        return f"{self.user.username} - {self.aparelho.exercise_name} ({self.rating} estrelas)"

class Visualizacao(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visualizacoes')
    aparelho = models.ForeignKey(Aparelho, on_delete=models.CASCADE, related_name='visualizacoes')
    count = models.PositiveIntegerField(default=1, help_text="Número de visualizações")
    viewed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_clicked = models.DateTimeField(null=True, blank=True, help_text="Última vez que o usuário clicou no botão")
    
    class Meta:
        ordering = ["-viewed_at"]
        unique_together = ['user', 'aparelho']  # Evita contagem duplicada
    
    def __str__(self):
        return f"{self.user.username} visualizou {self.aparelho.exercise_name} ({self.count}x)"
    
    def can_click_again(self):
        """Verifica se o usuário pode clicar novamente (cooldown de 1min30s)"""
        if not self.last_clicked:
            return True
        
        from django.utils import timezone
        from datetime import timedelta
        
        cooldown_time = self.last_clicked + timedelta(minutes=1, seconds=30)
        return timezone.now() > cooldown_time
    
    def get_remaining_cooldown(self):
        """Retorna o tempo restante do cooldown em segundos"""
        if not self.last_clicked:
            return 0
            
        from django.utils import timezone
        from datetime import timedelta
        
        cooldown_time = self.last_clicked + timedelta(minutes=1, seconds=30)
        remaining = cooldown_time - timezone.now()
        return max(0, int(remaining.total_seconds()))

