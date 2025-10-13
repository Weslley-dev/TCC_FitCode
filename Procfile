# Render.com deploy configuration
web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn app.wsgi:application
