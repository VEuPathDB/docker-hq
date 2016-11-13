#!/bin/bash

project=$1

cd "$project"

#export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-mysite.settings.production} 

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

exec python manage.py runserver 0.0.0.0:8000

#echo "Starting Gunicorn for '$project'".
#exec gunicorn "${project}.wsgi:application" \
#  --bind 0.0.0.0:8000 \
#  --workers 3
