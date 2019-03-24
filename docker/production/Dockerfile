FROM python:3.7.2-alpine

WORKDIR /app

COPY /requirements /app/requirements
COPY /manage.py /app/manage.py
COPY /project /app/project

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
    && pip install --no-cache-dir -r requirements/production.txt \
    && apk del .build-deps \
    && rm -vrf /var/cache/apk/*

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.5.0/wait /wait
RUN chmod +x /wait

CMD python manage.py collectstatic --noinput --clear && /wait && gunicorn project.wsgi -b :8000
