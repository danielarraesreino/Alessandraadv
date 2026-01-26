release: python manage.py migrate --noinput && python manage.py populate_articles && python manage.py create_demo_users
web: gunicorn --bind 0.0.0.0:$PORT --pythonpath src core.wsgi:application --timeout 120
