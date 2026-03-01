#!/usr/bin/env bash
# utility to start the project using the production settings locally
# it loads the .env file, migrates the database, collects static files and
# launches a WSGI server (gunicorn on UNIX, Django runserver on Windows).

set -euo pipefail

# load environment variables from .env if it exists
if [ -f ".env" ]; then
  # shellcheck disable=SC2046
  export $(grep -v '^#' .env | xargs)
fi

# make sure we use the prod settings even if manage.py defaults to them
export DJANGO_SETTINGS_MODULE=config.settings.prod

# install Python dependencies in case the virtual environment hasn't been
# prepared yet. this is cheap if they're already satisfied.
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

# start a simple production-like server on port 8000
# you can override PORT by exporting it before running this script
PORT=${PORT:-8000}

# gunicorn depends on fcntl which is not available on Windows.  fall back to
# Django's runserver there (acceptable for local testing).
# you could also install ``waitress`` or another cross-platform WSGI server.
if python - <<'PYTHON' >/dev/null 2>&1
import platform, sys
if platform.system().lower().startswith('windows'):
    sys.exit(0)
sys.exit(1)
PYTHON
then
  echo "Detected Windows platform, using Django development server instead of gunicorn."
  exec python manage.py runserver 0.0.0.0:${PORT}
else
  echo "Starting gunicorn on port ${PORT}"
  exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT}
fi
