#!/bin/bash

set -e

PROJECT_DIR="project/"
DOCKER_COMPOSE="docker-compose run --no-deps --rm web"

echo "Checking bandit..."
$DOCKER_COMPOSE bandit -rq -x **/tests/** $PROJECT_DIR

echo "Checking isort..."
$DOCKER_COMPOSE isort -rc -c $PROJECT_DIR

echo "Checking black..."
$DOCKER_COMPOSE black --check $PROJECT_DIR

echo "Checking flake8..."
$DOCKER_COMPOSE flake8 $PROJECT_DIR

echo "Checking terraform fmt..."
terraform fmt -check=true terraform
