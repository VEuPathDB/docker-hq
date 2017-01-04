Warning: These notes are not complete, possibly wrong in places.

## Production Admin

See `hq` entry in Passpack

## Development Deployment

`settings_local.py` is the place for site-specific configuration, including sensitive data such as passwords. The populated file is outside of the `hq` project so it survives across image upgrades and so it does not get committed to SCM. It is mounted on the running docker image.

    cd docker-hq
    cp hq/hq/settings/settings_local.py.sample settings_local.py

Edit `settings_local.py`.

Run the docker image:

    docker-compose up

In `docker-compose.yml` the `docker-hq` directory on the host is mounted on the image at `/usr/src/app`. This will override the contents of `/usr/src/app` that is burned into the image and allow real-time editing of the Django code. When you `docker build`, the edited code will be copied into the new image. Production deployments do not override the contents of `app`, and so run off the image code.

The sqlite database is in the `django-hq/data` directory.

### Build New Image

    docker build -t mheiges/hq .
    docker push mheiges/hq

## Production Deployment

When hosting on Linux servers, the `settings_local.py` file is mounted from the host's `/var/lib/hq/settings_local.py`.

By default the project runs under the hq.settings.production configuration. Here we set `-e DJANGO_SETTINGS_MODULE` value to use the production settings file.

### Deployment

See Puppet `profiles::hq`

### Restarting containers

As root

    # cd /var/lib/hq
    # docker-compose down
    # docker-compose up -d

## Misc

Static files are served directly from the django app using
[WhiteNoise](http://whitenoise.evans.io/). This avoids having to manage
another process (Nginx) to serve static content.