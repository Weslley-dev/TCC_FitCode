from django.db import models

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

    class Meta:
        ordering = ["exercise_name"]

    def __str__(self):
        return self.exercise_name or "Sem nome"

