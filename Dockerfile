FROM python:3.5.2-alpine

ENV DJANGO_SETTINGS_MODULE=hq.settings.production

RUN  apk --no-cache add  openldap-dev

RUN apk --no-cache add curl && \
  curl -sSL https://eupathdb.org/common/apidb-ca-rsa.crt \
  -o /usr/local/share/ca-certificates/apidb-ca-rsa.crt && \
  mkdir -p /etc/openldap/ && \
  echo 'TLS_CACERTDIR /etc/ssl/certs' >> /etc/openldap/ldap.conf && \
  apk del curl && \
  /usr/sbin/update-ca-certificates

WORKDIR /usr/src/app
RUN mkdir -p /usr/src/app

COPY hq /usr/src/app/hq

RUN apk --no-cache add git gcc musl-dev linux-headers && \
  pip install --no-cache-dir -r /usr/src/app/hq/requirements.txt && \
  apk del git gcc musl-dev linux-headers

COPY start_django.sh start_rqworker.sh start_rqscheduler.sh start_rqdashboard.sh /

EXPOSE 8000

CMD ["/start_django.sh", "hq"]
