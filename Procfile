# Render.com deploy configuration
web: python manage.py migrate && python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('WeslleyTcc', 'weslleypereira307@gmail.com', 'FitCode2024!') if not User.objects.filter(username='WeslleyTcc').exists() else None" && gunicorn app.wsgi:application
