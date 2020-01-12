#!/bin/bash

set -e

find . -name "*.pyc" -delete
scripts/wait.sh
docker-compose run --rm -e ENV=test -e TMDB_API_KEY= web pytest "$@"
