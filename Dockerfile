FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "mkdir -p /home/data && python manage.py migrate --noinput && gunicorn travelukraine_django.wsgi:application --bind 0.0.0.0:8000"]
