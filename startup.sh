python manage.py migrate --noinput
python manage.py seed_places
python manage.py collectstatic --noinput
gunicorn travelukraine_django.wsgi:application --bind=0.0.0.0
