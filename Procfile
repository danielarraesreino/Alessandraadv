web: python scripts/production_fix.py && cd src && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --log-level debug --access-logfile - --error-logfile -
