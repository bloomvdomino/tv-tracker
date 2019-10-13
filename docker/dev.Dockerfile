FROM python:3.7.4-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY /requirements-dev.txt /app/requirements-dev.txt
COPY /requirements.txt /app/requirements.txt

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
    && pip install --no-cache-dir -r requirements-dev.txt \
    # Install shfmt.
    && curl -sLo /bin/shfmt https://github.com/mvdan/sh/releases/download/v2.6.4/shfmt_v2.6.4_linux_amd64 \
    && chmod +x /bin/shfmt \
    # Install hadolint
    && curl -sLo /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v1.17.2/hadolint-Linux-x86_64 \
    && chmod +x /bin/hadolint \
    # Install terraform.
    && curl -sLo /tmp/tf.zip https://releases.hashicorp.com/terraform/0.12.8/terraform_0.12.8_linux_amd64.zip \
    && unzip /tmp/tf.zip -d /bin \
    && rm -vf /tmp/tf.zip \
    # Delete build dependencies.
    && apk del .build-deps \
    && rm -vrf /var/cache/apk/*

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.6.0/wait /wait
RUN chmod +x /wait

CMD ["sh", "scripts/start-dev.sh"]
