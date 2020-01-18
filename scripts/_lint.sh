#!/bin/bash

set -e

echo "Running linters:"

echo "shfmt..."
shfmt -d -p -i=4 scripts

echo "hadolint..."
hadolint Dockerfile

echo "bandit..."
bandit -rq -x **/tests/** project

echo "isort..."
isort -rc -c .

echo "black..."
black --check .

echo "flake8..."
flake8 .

echo "terraform..."
terraform fmt -recursive -check=true terraform
