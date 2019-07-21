#!/bin/bash

set -e

PROJECT_DIR="project/"
TERRAFORM_DIR="terraform/"

DOCKER_COMPOSE="docker-compose run --no-deps --rm web"

echo "Running bandit..."
$DOCKER_COMPOSE bandit -rq -x **/tests/** $PROJECT_DIR

if [ $# = 1 ] && [ $1 = "--check" ]
then
    echo "Running isort..."
    $DOCKER_COMPOSE isort -rc -c $PROJECT_DIR

    echo "Running black..."
    $DOCKER_COMPOSE black --check $PROJECT_DIR

    echo "Running flake8..."
    $DOCKER_COMPOSE flake8 $PROJECT_DIR

    echo "Running terraform fmt..."
    terraform fmt -check=true $TERRAFORM_DIR
else
    echo "Running isort..."
    $DOCKER_COMPOSE isort -rc $PROJECT_DIR

    echo "Running black..."
    $DOCKER_COMPOSE black $PROJECT_DIR

    echo "Running flake8..."
    $DOCKER_COMPOSE flake8 $PROJECT_DIR

    echo "Running terraform fmt..."
    terraform fmt $TERRAFORM_DIR
fi
