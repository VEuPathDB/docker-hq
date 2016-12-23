superuser: admin/adminadmin

      docker build -t ebrc/hq .

## Development Deployment

`settings_local.py` is the place for site-specific configuration, including sensitive data such as passwords. The populated file is outside of the `hq` project so it survives across image upgrades and so it does not get committed to SCM. It is mounted on the running docker image.

    cd docker-hq
    cp hq/hq/settings/settings_local.py.sample settings_local.py

Edit `settings_local.py`.

Run the docker image:

    docker run -it --rm -p 8111:8000 -v /Users/mheiges/Docker/docker-hq/settings_local.py:/usr/src/app/hq/hq/settings/settings_local.py -v /Users/mheiges/Docker/docker-hq:/usr/src/app -e DJANGO_SETTINGS_MODULE=hq.settings.development --name hq mheiges/hq 

In this invocation the `docker-hq` on the host is mounted on the image at `/usr/src/app`. This will override the contents of `/usr/src/app` that is burned into the image and allow real-time editing of the Django code. When you `docker build`, the edited code will be copied into the new image. Production deployments do not override the contents of `app`, so run off the image code.

The sqlite database is in the `django-hq/data` directory.

### Build New Image

    docker build -t mheiges/hq .
    docker push mheiges/hq

## Production Deployment

When hosting on Linux servers, the `settings_local.py` file is mounted from the host's `/var/lib/hq/settings_local.py`.


/usr/bin/docker run -t -e DJANGO_SETTINGS_MODULE=hq.settings.production -p 8111:8000 -v /var/lib/hq/settings_local.py:/usr/src/app/hq/hq/settings/settings_local.py -v /var/lib/hq/data:/usr/src/app/data --name hq mheiges/hq

By default the project runs under the hq.settings.production configuration. Here we set `-e DJANGO_SETTINGS_MODULE` value to use the production settings file.

      $ docker run -it --rm -p 8000:8000 -v /Users/mheiges/Docker/docker-hq:/usr/src/app --name hq -e DJANGO_SETTINGS_MODULE=hq.settings.development ebrc/hq

### Deployment

See Puppet `profiles::hq`

### Restarting container

    systemctl restart docker-hq.service 

## Misc

Static files are served directly from the django app using
[WhiteNoise](http://whitenoise.evans.io/). This avoids having to manage
another process (Nginx) to serve static content.