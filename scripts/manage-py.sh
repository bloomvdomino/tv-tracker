#!/bin/bash

set -e

sh scripts/wait.sh
docker-compose run web python manage.py "$@"
