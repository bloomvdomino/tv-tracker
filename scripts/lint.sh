#!/bin/bash

set -e

echo "Running flake8."
docker-compose run --no-deps web flake8 project
