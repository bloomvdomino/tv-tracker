#!/bin/bash

set -e

DOCKER_COMPOSE="docker-compose run --no-deps --rm web"

echo "Running shfmt..."
$DOCKER_COMPOSE shfmt -l -w -p -i=4 scripts

echo "Running isort..."
$DOCKER_COMPOSE isort -rc .

echo "Running black..."
$DOCKER_COMPOSE black .

echo "Running terraform fmt..."
$DOCKER_COMPOSE terraform fmt -recursive terraform
