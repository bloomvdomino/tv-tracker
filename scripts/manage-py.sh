#!/bin/bash

set -e

sh scripts/wait.sh
sh scripts/docker-compose.sh run --rm web python manage.py "$@"
