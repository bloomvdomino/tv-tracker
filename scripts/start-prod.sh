#!/bin/bash

set -e

python manage.py collectstatic --noinput --clear
gunicorn project.wsgi --config gunicorn.py
