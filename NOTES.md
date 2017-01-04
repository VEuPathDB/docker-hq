Mount
    -v /Users/mheiges/Docker/docker-hq/settings_local.py:/usr/src/app/hq/hq/settings/settings_local.py




Following the tutorial at
https://docs.djangoproject.com/en/1.10/intro/tutorial01/


The tutorial uses an official Python Dockerfile, documented at
https://hub.docker.com/_/python/

The tutorial starts with having you install Django and Gunicorn on the host system so you can create a starter project (`django-admin.py startproject`). I prefer to leverage Docker for that so I don't have to deal with conflicts and dependencies on the host (isn't this one of the driving benefits behind Docker?), so there will be a small change to the tutorial.

Create Dockerfile as documented in tutorial, then build the docker image

    docker build -t ebrc/djangodemo .


The [`python:2-onbuild`](https://github.com/docker-library/python/blob/master/2.7/onbuild/Dockerfile) container will pip install the packages listed in `requirements.txt`.

To initialize the `mysite` starter project we run `django-admin.py startproject` within that new Docker contaner. 

    docker run -it --rm -e DJANGO_SETTINGS_MODULE='' -v "$PWD":/usr/src/app ebrc/djangodemo django-admin.py startproject mysite

Running docker this way will run the django command specified rather than the `CMD` in the Dockerfile. We mapped the current host directory to the working directory on the Docker image so the newly created Django project is persistent on the host and available for editing.

After `django-admin` creates the new `mysite` project Docker exits and removes the container (`--rm`).

Now we can resume the tutorial by editing the `mysite` project as desired and starting the container and Django app.

    docker run --rm -it -p 8000:8000 -v /Users/mheiges/Docker/docker-djangodemo:/usr/src/app --name djangodemo ebrc/djangodemo


Create directory structure for Poll app

    docker run -it --rm -v "$PWD":/usr/src/app -w /usr/src/app/mysite ebrc/djangodemo python manage.py startapp polls


Migrate

    docker exec djangodemo /bin/bash -c 'cd /usr/src/app/mysite && python manage.py migrate'

Activate Model

    docker exec djangodemo /bin/bash -c 'cd /usr/src/app/mysite && python manage.py makemigrations polls'


Create Admin User

    docker exec -it djangodemo /bin/bash -c 'cd /usr/src/app/mysite && python manage.py createsuperuser'
