#!/bin/bash

set -e

python manage.py migrate
python manage.py collectstatic --noinput --clear

gunicorn project.wsgi
