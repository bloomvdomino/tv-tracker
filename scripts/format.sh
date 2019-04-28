#!/bin/bash

set -e

project_dir="project/"
terraform_dir="terraform/"

isort="sh scripts/docker-compose.sh run --no-deps --rm web isort -rc"
black="sh scripts/docker-compose.sh run --no-deps --rm web black"

if [ $# = 1 ] && [ $1 = "--check" ]
then
    echo "Running isort..."
    $isort -c $project_dir

    echo "Running black..."
    $black --check $project_dir

    echo "Running flake8..."
    sh scripts/docker-compose.sh run --no-deps --rm web flake8 $project_dir

    echo "Running terraform fmt..."
    terraform fmt -check=true $terraform_dir
else
    echo "Running isort..."
    $isort $project_dir

    echo "Running black..."
    $black $project_dir

    echo "Running terraform fmt..."
    terraform fmt $terraform_dir
fi
