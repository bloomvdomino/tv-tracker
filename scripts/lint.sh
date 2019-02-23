#!/bin/bash

set -e

echo "Running isort"
docker-compose run --no-deps web isort -rc project

echo "Running flake8"
docker-compose run --no-deps web flake8 project
