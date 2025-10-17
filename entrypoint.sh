#!/bin/sh

python manage.py migrate --noinput

python manage.py collectstatic --noinput

python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email="admin@example.com").exists():
    User.objects.create_superuser(email="admin@example.com", username="admin", password="admin123")
    print("Superuser created (admin@example.com)")
else:
    print("Superuser alredy exists.")
END

python manage.py shell -c "from django.core.cache import cache; cache.clear()"

export PYTHONUNBUFFERED=1

exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 2 --timeout 300 --preload
