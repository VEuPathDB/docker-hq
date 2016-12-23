FROM python:3

ENV DJANGO_SETTINGS_MODULE=hq.settings.production

WORKDIR /usr/src/app
RUN mkdir -p /usr/src/app

RUN apt-get update && apt-get install -y libldap2-dev libsasl2-dev libssl-dev

COPY hq /usr/src/app/hq
RUN pip install --no-cache-dir -r /usr/src/app/hq/requirements.txt

RUN curl -sSL https://eupathdb.org/common/apidb-ca-rsa.crt \
  -o /usr/local/share/ca-certificates/apidb-ca-rsa.crt
RUN /usr/sbin/update-ca-certificates

COPY start.sh /start.sh

EXPOSE 8000

CMD ["/start.sh", "hq"]
