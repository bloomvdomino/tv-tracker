#!/bin/bash

# https://devcenter.heroku.com/articles/container-registry-and-runtime

set -e

if [ $# -ne 1 ]; then
    exit 1
fi

ENV=$1

APP=tv-tracker-olivertso
if [ $ENV != production ]; then
    APP=$APP-$ENV
fi

PROCESS_TYPE=web
REGISTRY=registry.heroku.com
TAG=$REGISTRY/$APP/$PROCESS_TYPE

echo $HEROKU_API_KEY | docker login --username=_ --password-stdin $REGISTRY
docker build -f docker/prod.Dockerfile -t $TAG .
docker push $TAG
docker rmi $(docker images $TAG -q)
heroku container:release -a $APP $PROCESS_TYPE

if [ $ENV != production ]; then
    heroku pg:reset -a $APP DATABASE --confirm $APP
fi

heroku run -a $APP python manage.py migrate
