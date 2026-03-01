#!/bin/bash
# Vercel build script for Django

pip install setuptools


echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

# optionally mirror the collected assets into the vercel output folder so the
# platform can serve them directly. Django/whitenoise will work without this
# too, but the static route becomes unnecessary once the files live here.
mkdir -p .vercel_output/static
cp -R staticfiles/* .vercel_output/static/

echo "Build complete!"
