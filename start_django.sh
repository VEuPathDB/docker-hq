#!/bin/sh

project=$1

cd "$project"

if ! grep -q '128.192.75.30' /etc/hosts; then
  echo '128.192.75.30 ds1.apidb.org' >> /etc/hosts
fi

export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-hq.settings.production}
echo "Using DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}"

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate


if [ $DJANGO_SETTINGS_MODULE == "hq.settings.production" ]; then
  echo "Starting Gunicorn for '$project'".
  exec gunicorn "${project}.wsgi:application" \
    --bind 0.0.0.0:8000 \
    --workers 3
else
  exec python manage.py runserver 0.0.0.0:8000
fi