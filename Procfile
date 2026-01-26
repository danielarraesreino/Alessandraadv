release: python manage.py migrate --noinput && python manage.py populate_articles && python manage.py create_demo_users && python .agent/skills/db-manager/scripts/validate_schema.py
web: python manage.py collectstatic --noinput && cd src && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --log-level debug --access-logfile - --error-logfile -
