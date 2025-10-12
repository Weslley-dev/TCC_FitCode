#!/usr/bin/env python
"""
Script para limpar aparelhos duplicados
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from aparelhos.models import Aparelho
from django.db.models import Count

def clean_duplicates():
    print("🧹 Limpando aparelhos duplicados...")
    
    # Encontrar duplicados
    duplicados = Aparelho.objects.values('exercise_name').annotate(count=Count('id')).filter(count__gt=1)
    
    print(f"Encontrados {len(duplicados)} nomes duplicados:")
    for item in duplicados:
        print(f"  - {item['exercise_name']}: {item['count']} cópias")
    
    # Remover duplicados (manter apenas o primeiro)
    for item in duplicados:
        exercise_name = item['exercise_name']
        aparelhos = Aparelho.objects.filter(exercise_name=exercise_name).order_by('id')
        
        # Manter o primeiro, remover os outros
        aparelhos_to_remove = aparelhos[1:]
        for aparelho in aparelhos_to_remove:
            print(f"  🗑️ Removendo duplicado: {aparelho.exercise_name} (ID: {aparelho.id})")
            aparelho.delete()
    
    print(f"✅ Limpeza concluída! Total de aparelhos: {Aparelho.objects.count()}")

if __name__ == "__main__":
    clean_duplicates()
