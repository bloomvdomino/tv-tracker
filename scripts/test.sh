#!/bin/bash

set -e

find . -name "*.pyc" -delete
sh scripts/wait.sh
docker-compose run -e ENV=test web pytest "$@"
