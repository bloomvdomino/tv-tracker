#!/bin/bash

set -e

docker-compose-wait
gunicorn project.wsgi \
    --config gunicorn.py \
    --reload \
    --access-logfile - \
    --access-logformat "%(t)s %(r)s %(s)s %(b)s"
