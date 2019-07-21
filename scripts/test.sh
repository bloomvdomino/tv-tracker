#!/bin/bash

set -e

find . -name "*.pyc" -delete
sh scripts/wait.sh
docker-compose run --rm -e ENV=test -e TMDB_API_KEY= web pytest "$@"
