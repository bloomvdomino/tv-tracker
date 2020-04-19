# BASE
FROM python:3.8.2-slim AS base

WORKDIR /app

RUN useradd -m appuser && chown -R appuser:appuser /home/appuser

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y gcc && rm -vrf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install --no-cache-dir --disable-pip-version-check --require-hashes -r requirements.txt \
    && apt-get purge -y --auto-remove gcc

# PRODUCTION
FROM base AS production

COPY manage.py manage.py
COPY gunicorn.py gunicorn.py
COPY bin/start_prod bin/start_prod
COPY project project

USER appuser

CMD ["bin/start_prod"]

# DEVELOPMENT
FROM base AS development

RUN apt-get update && apt-get install -y unzip

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /usr/local/bin/docker-compose-wait
RUN chmod +x /usr/local/bin/docker-compose-wait

ADD https://releases.hashicorp.com/terraform/0.12.23/terraform_0.12.23_linux_amd64.zip /tmp/terraform.zip
RUN unzip /tmp/terraform.zip -d /usr/local/bin && rm -vf /tmp/terraform.zip

COPY requirements-dev.txt requirements-dev.txt
RUN pip install --no-cache-dir --disable-pip-version-check --require-hashes -r requirements-dev.txt

USER appuser

CMD ["bin/start_dev"]
