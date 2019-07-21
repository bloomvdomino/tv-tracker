#!/bin/bash

set -e

TAG=$DOCKER_USERNAME/tv-tracker

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker build -f docker/prod.Dockerfile -t $TAG .
docker push $TAG
