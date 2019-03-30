#!/bin/bash

set -e

echo "Running isort"
sh scripts/docker-compose.sh run --no-deps --rm web isort -rc project

echo "Running flake8"
sh scripts/docker-compose.sh run --no-deps --rm web flake8 project

echo "Running terraform fmt"
terraform fmt
