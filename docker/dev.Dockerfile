FROM python:3.7.4-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY /requirements /app/requirements
COPY /manage.py /app/manage.py

RUN apk update \
    && apk add --no-cache libpq postgresql-client \
    && apk add --no-cache --virtual .build-deps \
        curl \
        gcc \
        libffi-dev \
        make \
        musl-dev \
        openssl-dev \
        postgresql-dev \
    && pip install --no-cache-dir --upgrade pip setuptools \
    && pip install --no-cache-dir -r requirements/development.txt \
    # Install terraform.
    && curl -sLo /tmp/tf.zip https://releases.hashicorp.com/terraform/0.12.8/terraform_0.12.8_linux_amd64.zip \
    && unzip /tmp/tf.zip -d /bin \
    && rm -vf /tmp/tf.zip \
    # Delete install dependencies.
    && apk del .build-deps \
    && rm -vrf /var/cache/apk/*

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.5.1/wait /wait
RUN chmod +x /wait

CMD /wait && python manage.py runserver 0:8000
