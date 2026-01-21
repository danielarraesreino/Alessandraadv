release: python manage.py migrate --noinput && python manage.py populate_articles
web: cd src && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --log-level debug --access-logfile - --error-logfile -
