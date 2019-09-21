#!/bin/bash

set -e

DOCKER_COMPOSE="docker-compose run --no-deps --rm web"

echo "Running isort..."
$DOCKER_COMPOSE isort -rc project

echo "Running black..."
$DOCKER_COMPOSE black project

echo "Running terraform fmt..."
$DOCKER_COMPOSE terraform fmt -recursive terraform
