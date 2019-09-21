#!/bin/bash

set -e

DOCKER_COMPOSE="docker-compose run --no-deps --rm web"

echo "Checking bandit..."
$DOCKER_COMPOSE bandit -rq -x **/tests/** project

echo "Checking isort..."
$DOCKER_COMPOSE isort -rc -c .

echo "Checking black..."
$DOCKER_COMPOSE black --check .

echo "Checking flake8..."
$DOCKER_COMPOSE flake8 .

echo "Checking terraform fmt..."
$DOCKER_COMPOSE terraform fmt -recursive -check=true terraform
