FROM python:3.7.2-alpine

RUN adduser -D ttuser

WORKDIR /app

COPY /requirements /app/requirements
COPY /gunicorn.py /app/gunicorn.py
COPY /manage.py /app/manage.py
COPY /project /app/project

RUN mkdir /app/staticfiles && chown -R ttuser:ttuser /app/staticfiles \
    && apk update \
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

USER ttuser

CMD python manage.py collectstatic --noinput --clear && gunicorn project.wsgi -c gunicorn.py
