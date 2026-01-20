web: cd src && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
release: cd src && python manage.py migrate --noinput
