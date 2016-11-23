superuser: admin/adminadmin

      docker build -t ebrc/djangodemo .

      $ docker run -it --rm -p 8000:8000 -v /Users/mheiges/Docker/docker-djangodemo:/usr/src/app --name djangodemo ebrc/djangodemo

By default the project runs under the mysite.settings.production configuration. Set `-e DJANGO_SETTINGS_MODULE` value to use a different settings file.

      $ docker run -it --rm -p 8000:8000 -v /Users/mheiges/Docker/docker-djangodemo:/usr/src/app --name djangodemo -e DJANGO_SETTINGS_MODULE=mysite.settings.development ebrc/djangodemo
