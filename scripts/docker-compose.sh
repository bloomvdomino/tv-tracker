#!/bin/bash

set -e

docker-compose -f docker/docker-compose.yml -f docker/development/docker-compose.yml -p tv-tracker "$@"
