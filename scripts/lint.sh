#!/bin/bash

set -e

echo "Running isort"
docker-compose run --no-deps --rm web isort -rc project

echo "Running flake8"
docker-compose run --no-deps --rm web flake8 project
