#!/bin/bash

set -e

sh scripts/docker-compose.sh run --rm web /wait
