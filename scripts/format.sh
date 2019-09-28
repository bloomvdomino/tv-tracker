#!/bin/bash

set -e

DOCKER_COMPOSE="docker-compose run --no-deps --rm web"

echo "Running formatters:"

echo "shfmt..."
$DOCKER_COMPOSE shfmt -l -w -p -i=4 scripts

echo "isort..."
$DOCKER_COMPOSE isort -rc .

echo "black..."
$DOCKER_COMPOSE black .

echo "terraform..."
$DOCKER_COMPOSE terraform fmt -recursive terraform
