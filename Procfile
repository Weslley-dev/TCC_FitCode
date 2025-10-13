# Render.com deploy configuration
web: python manage.py migrate && python configure_render_postgres.py && gunicorn app.wsgi:application
