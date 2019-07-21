FROM python:3.7.2-alpine

WORKDIR /app

COPY /requirements /app/requirements
COPY /gunicorn.py /app/gunicorn.py
COPY /manage.py /app/manage.py
COPY /project /app/project

RUN apk update \
    && apk add --no-cache libpq postgresql-client \
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

CMD python manage.py collectstatic --noinput --clear \
    && python manage.py migrate \
    && gunicorn project.wsgi -c gunicorn.py