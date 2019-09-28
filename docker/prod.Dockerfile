FROM python:3.7.4-alpine

RUN adduser -D ttuser

WORKDIR /app

COPY /requirements /app/requirements
COPY /gunicorn.py /app/gunicorn.py
COPY /manage.py /app/manage.py
COPY /project /app/project
COPY /scripts/start-prod.sh /app/scripts/start-prod.sh

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

CMD ["sh", "scripts/start-prod.sh"]
