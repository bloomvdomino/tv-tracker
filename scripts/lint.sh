#!/bin/bash

set -e

isort () {
    echo "Running isort"
    sh scripts/docker-compose.sh run --no-deps --rm web isort -rc project
}

flake8 () {
    echo "Running flake8"
    sh scripts/docker-compose.sh run --no-deps --rm web flake8 project
}

terraform_fmt () {
    echo "Running terraform fmt"
    terraform fmt terraform/
}

if [ $# == 0 ]
then
    isort
    flake8
    terraform_fmt
else
    for arg in $@
    do
        if [ $arg = "isort" ]; then
            isort
        fi
        if [ $arg = "flake8" ]; then
            flake8
        fi
        if [ $arg = "terraform" ]; then
            terraform_fmt
        fi
    done
fi
