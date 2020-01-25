#!/bin/bash

set -e

export ENV=test
export TMDB_API_KEY=""

find . -name "*.pyc" -delete
docker-compose-wait
pytest "$@"
