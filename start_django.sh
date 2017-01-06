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
  echo "Starting uwsgi for '$project'".
  exec uwsgi --chdir="/usr/src/app/${project}" \
    --module=${project}.wsgi:application \
    --master --pidfile="/tmp/${project}-master.pid" \
    --http=0.0.0.0:8000 \
    --processes=5 \
    --harakiri=20 \
    --max-requests=5000 \
    --vacuum
else
  exec python manage.py runserver 0.0.0.0:8000
fi
