#!/bin/bash

set -e

docker-compose run -e ENV=test web pytest "$@"
