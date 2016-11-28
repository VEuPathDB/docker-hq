
FROM python:3

ENV DJANGO_SETTINGS_MODULE=hq.settings.production

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y libldap2-dev libsasl2-dev libssl-dev

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

RUN curl -sSL https://eupathdb.org/common/apidb-ca-rsa.crt \
  -o /usr/local/share/ca-certificates/apidb-ca-rsa.crt
RUN /usr/sbin/update-ca-certificates

COPY . /usr/src/app

RUN python hq/manage.py migrate

COPY start.sh /start.sh

EXPOSE 8000

CMD ["/start.sh", "hq"]
