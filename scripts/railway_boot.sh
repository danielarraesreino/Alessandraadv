#!/bin/bash
echo ">>> RAILWAY BOOT SCRIPT STARTING <<<"
echo ">>> Current User: $(whoami) <<<"
echo ">>> Current Path: $(pwd) <<<"
echo ">>> Python Version: $(python --version) <<<"
echo ">>> Port: $PORT <<<"

# Run migrations in the background (or foreground before starting)
echo ">>> Running Migrations <<<"
python manage.py migrate --noinput

echo ">>> Starting Gunicorn <<<"
exec gunicorn --chdir src core.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --timeout 120 \
    --log-level debug \
    --access-logfile - \
    --error-logfile -
