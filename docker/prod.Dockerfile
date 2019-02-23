FROM python:3.7.2-alpine

WORKDIR /app

COPY /docker/prod-cmd.sh /prod-cmd.sh
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
    && pip install --no-cache-dir -r requirements/prod.txt \
    && apk del .build-deps \
    && rm -vrf /var/cache/apk/*

CMD sh /prod-cmd.sh
