#!/bin/bash

set -e

find . -name "*.pyc" -delete
sh scripts/wait.sh
sh scripts/docker-compose.sh run --rm -e ENV=test web pytest "$@"
