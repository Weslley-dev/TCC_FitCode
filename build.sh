#!/usr/bin/env bash
# Script de build para Render.com

echo "Iniciando build..."

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

echo "Build concluído!"
