#!/bin/bash

set -e

python manage.py collectstatic --noinput --clear
gunicorn project.wsgi -c gunicorn.py
