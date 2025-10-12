#!/usr/bin/env bash
# Script de build para Render.com

echo "Iniciando build..."

# Instalar dependências
pip install -r requirements.txt

# Executar migrações com verbosidade
echo "Executando migrações..."
python manage.py migrate --verbosity=2

# Verificar se as tabelas foram criadas
echo "Verificando banco de dados..."
python manage.py shell -c "from django.contrib.auth.models import User; print(f'Usuários: {User.objects.count()}')"

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Build concluído!"
