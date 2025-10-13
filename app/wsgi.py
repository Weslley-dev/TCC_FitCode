"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# Executar migrações no Render
if os.environ.get('RENDER'):
    try:
        django.setup()
        print("Executando migrações no startup...")
        call_command('migrate', verbosity=0)
        print("Migrações executadas com sucesso!")
    except Exception as e:
        print(f"Erro ao executar migrações: {e}")

application = get_wsgi_application()
