#!/bin/bash

set -e

docker-compose-wait
python manage.py runserver 0:8000
