web: gunicorn --chdir src core.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --log-level debug --access-logfile - --error-logfile -
release: python manage.py migrate --noinput
