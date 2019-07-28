#!/bin/bash

set -e

ENV=production
APP=tv-tracker
TAG=$DOCKER_USERNAME/$APP

# Build and push Docker image.
echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
docker build -f docker/prod.Dockerfile -t $TAG .
docker push $TAG

# Replace ECS task.
CLUSTER=$(aws ecs list-clusters | grep hobby-infra-$ENV | sed 's/"//g' | awk '{$1=$1};1')
TASK=$(aws ecs list-tasks \
    --cluster $CLUSTER \
    --service-name $APP-$ENV \
    | grep arn:aws:ecs \
    | sed 's/"//g' \
    | awk '{$1=$1};1')
aws ecs stop-task --cluster $CLUSTER --task $TASK --reason Deploy
