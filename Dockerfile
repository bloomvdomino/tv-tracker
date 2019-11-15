FROM python:3.7.4-alpine AS production

WORKDIR /app

# Install system dependencies.
RUN apk update --no-cache && apk add --no-cache libpq postgresql-client

COPY /requirements.txt ./requirements.txt
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
    # Install PIP dependencies.
    && pip install --no-cache-dir --upgrade pip setuptools \
    && pip install --no-cache-dir -r requirements.txt \
    # Delete build dependencies.
    && apk del .build-deps

COPY /manage.py ./manage.py
COPY /gunicorn.py ./gunicorn.py
COPY /scripts/start-prod.sh ./scripts/start-prod.sh
COPY /project ./project

RUN adduser -D ttuser && mkdir ./staticfiles && chown -R ttuser:ttuser ./staticfiles
USER ttuser

CMD ["sh", "scripts/start-prod.sh"]

FROM production AS development

ENV PYTHONUNBUFFERED 1

USER root

WORKDIR /app

COPY /requirements-dev.txt ./requirements-dev.txt
RUN apk add --no-cache --virtual .build-deps curl \
    # Install PIP dependencies.
    && pip install --no-cache-dir -r requirements-dev.txt \
    # Install docker compose wait.
    && curl -sLo /bin/docker-compose-wait https://github.com/ufoscout/docker-compose-wait/releases/download/2.6.0/wait \
    && chmod +x /bin/docker-compose-wait \
    # Install shfmt.
    && curl -sLo /bin/shfmt https://github.com/mvdan/sh/releases/download/v2.6.4/shfmt_v2.6.4_linux_amd64 \
    && chmod +x /bin/shfmt \
    # Install hadolint.
    && curl -sLo /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.17.2/hadolint-Linux-x86_64 \
    && chmod +x /bin/hadolint \
    # Install terraform.
    && curl -sLo /tmp/tf.zip https://releases.hashicorp.com/terraform/0.12.8/terraform_0.12.8_linux_amd64.zip \
    && unzip /tmp/tf.zip -d /bin \
    && rm -vf /tmp/tf.zip \
    # Delete build dependencies.
    && apk del .build-deps

CMD ["sh", "scripts/start-dev.sh"]
