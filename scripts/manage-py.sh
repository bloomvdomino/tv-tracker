#!/bin/bash

set -e

docker-compose run web python manage.py "$@"
