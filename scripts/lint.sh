#!/bin/bash

set -e

DOCKER_COMPOSE="docker-compose run --no-deps --rm web"

echo "Running linters:"

echo "shfmt..."
$DOCKER_COMPOSE shfmt -d -p -i=4 scripts

echo "hadolint..."
$DOCKER_COMPOSE hadolint Dockerfile

echo "bandit..."
$DOCKER_COMPOSE bandit -rq -x **/tests/** project

echo "isort..."
$DOCKER_COMPOSE isort -rc -c .

echo "black..."
$DOCKER_COMPOSE black --check .

echo "flake8..."
$DOCKER_COMPOSE flake8 .

echo "terraform..."
$DOCKER_COMPOSE terraform fmt -recursive -check=true terraform
