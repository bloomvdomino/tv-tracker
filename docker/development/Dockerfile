FROM python:3.7.2-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY /requirements /app/requirements
COPY /manage.py /app/manage.py

RUN apk update \
    && apk add --no-cache libpq \
    && apk add --no-cache --virtual .build-deps \
        gcc \
        libffi-dev \
        make \
        musl-dev \
        openssl-dev \
        postgresql-dev \
    && pip install --no-cache-dir --upgrade pip setuptools \
    && pip install --no-cache-dir -r requirements/development.txt \
    && apk del .build-deps \
    && rm -vrf /var/cache/apk/*

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.5.0/wait /wait
RUN chmod +x /wait

CMD /wait && python manage.py runserver 0:8000
