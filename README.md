superuser: admin/adminadmin

      docker build -t ebrc/hq .

## Development

      $ docker run -it --rm -p 8000:8000 -v /Users/mheiges/Docker/docker-hq:/usr/src/app -e DJANGO_SETTINGS_MODULE=hq.settings.development --name hq ebrc/hq

## Production

      $ docker run -it --rm -p 8000:8000 -v /Users/mheiges/Docker/docker-hq:/usr/src/app --name hq ebrc/hq

By default the project runs under the hq.settings.production configuration. Set `-e DJANGO_SETTINGS_MODULE` value to use a different settings file.

      $ docker run -it --rm -p 8000:8000 -v /Users/mheiges/Docker/docker-hq:/usr/src/app --name hq -e DJANGO_SETTINGS_MODULE=hq.settings.development ebrc/hq


Static files are served directly from the django app using [WhiteNoise](http://whitenoise.evans.io/)