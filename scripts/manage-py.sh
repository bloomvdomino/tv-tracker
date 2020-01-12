#!/bin/bash

set -e

scripts/wait.sh
docker-compose run --rm web python manage.py "$@"
