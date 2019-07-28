#!/bin/bash

set -e

PROJECT_DIR="project/"
DOCKER_COMPOSE="docker-compose run --no-deps --rm web"

echo "Running isort..."
$DOCKER_COMPOSE isort -rc $PROJECT_DIR

echo "Running black..."
$DOCKER_COMPOSE black $PROJECT_DIR

echo "Running terraform fmt..."
terraform fmt terraform
