#!/bin/bash

set -e

echo "Running formatters:"

echo "shfmt..."
shfmt -l -w -p -i=4 scripts

echo "isort..."
isort -rc .

echo "black..."
black .

echo "terraform..."
terraform fmt -recursive terraform
