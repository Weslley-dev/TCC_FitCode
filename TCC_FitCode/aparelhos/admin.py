from django.contrib import admin
from aparelhos.models import Aparelho, Grupo_muscular

@admin.register(Grupo_muscular)
class GrupoMuscularAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Aparelho)
class AparelhoAdmin(admin.ModelAdmin):
    list_display = ('id', 'exercise_name', 'grupo_muscular', 'image', 'video')
    search_fields = ('exercise_name', 'instructions')
    list_filter = ('grupo_muscular',)
