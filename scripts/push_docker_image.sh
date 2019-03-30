#!/bin/bash

set -e

# Push production Docker image to Docker Hub.
tag=olivertso/tv-tracker
docker build -f docker/production/Dockerfile -t $tag .
docker push $tag
docker rmi $(docker images $tag -q)
