FROM python:3.7.4-alpine

RUN adduser -D ttuser

WORKDIR /app

COPY /requirements.txt ./requirements.txt

RUN mkdir ./staticfiles && chown -R ttuser:ttuser ./staticfiles \
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
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps \
    && rm -vrf /var/cache/apk/*

COPY /manage.py ./manage.py
COPY /gunicorn.py ./gunicorn.py
COPY /scripts/start-prod.sh ./scripts/start-prod.sh
COPY /project ./project

USER ttuser

CMD ["sh", "scripts/start-prod.sh"]
