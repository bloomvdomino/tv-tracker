#!/bin/bash

set -e

sh scripts/wait.sh
docker-compose run --rm web python manage.py "$@"
