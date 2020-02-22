FROM python:3.8.1-alpine3.11 AS production

WORKDIR /app

# Install system dependencies.
RUN apk update && apk add --no-cache libpq postgresql-client

COPY /requirements.txt ./requirements.txt
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
    && pip install --no-cache-dir --disable-pip-version-check --require-hashes -r requirements.txt \
    && apk del .build-deps

RUN rm -rf /var/cache/apk/*

COPY /manage.py ./manage.py
COPY /gunicorn.py ./gunicorn.py
COPY /bin/start-prod ./bin/start-prod
COPY /project ./project

RUN adduser -D ttuser && mkdir ./staticfiles && chown -R ttuser:ttuser ./staticfiles
USER ttuser

CMD ["bin/start-prod"]

FROM production AS development

ENV PYTHONUNBUFFERED 1

USER root

WORKDIR /app

RUN apk add --no-cache curl gcc musl-dev postgresql-dev

RUN \
    # Install docker compose wait.
    curl -sLo /bin/docker-compose-wait https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.2/wait \
    && chmod +x /bin/docker-compose-wait \
    # Install shfmt.
    && curl -sLo /bin/shfmt https://github.com/mvdan/sh/releases/download/v3.0.0/shfmt_v3.0.0_linux_amd64 \
    && chmod +x /bin/shfmt \
    # Install hadolint.
    && curl -sLo /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.17.3/hadolint-Linux-x86_64 \
    && chmod +x /bin/hadolint \
    # Install terraform.
    && curl -sLo /tmp/tf.zip https://releases.hashicorp.com/terraform/0.12.18/terraform_0.12.18_linux_amd64.zip \
    && unzip /tmp/tf.zip -d /bin \
    && rm -vf /tmp/tf.zip

COPY /requirements-dev.txt ./requirements-dev.txt
RUN pip install --no-cache-dir --disable-pip-version-check pip-tools \
    && pip install --no-cache-dir --disable-pip-version-check --require-hashes -r requirements-dev.txt

RUN rm -rf /var/cache/apk/*

USER ttuser

CMD ["bin/start-dev"]
