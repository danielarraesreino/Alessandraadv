release: python manage.py migrate --noinput && python manage.py populate_articles && python manage.py create_demo_users
web: python manage.py collectstatic --noinput && cd src && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --timeout 120
