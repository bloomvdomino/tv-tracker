#!/bin/bash

set -e

DOCKER_COMPOSE="docker-compose run --no-deps --rm web"

echo "Checking bandit..."
$DOCKER_COMPOSE bandit -rq -x **/tests/** project

echo "Checking isort..."
$DOCKER_COMPOSE isort -rc -c project

echo "Checking black..."
$DOCKER_COMPOSE black --check project

echo "Checking flake8..."
$DOCKER_COMPOSE flake8 project

echo "Checking terraform fmt..."
terraform fmt -recursive -check=true terraform
