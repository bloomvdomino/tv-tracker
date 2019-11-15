#!/bin/bash

set -e

docker-compose run --rm web docker-compose-wait
