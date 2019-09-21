#!/bin/bash

# https://devcenter.heroku.com/articles/container-registry-and-runtime

set -e

if [ $# -ne 1 ]; then
    exit 1
fi

APP=tv-tracker-olivertso
if [ $1 != production ]; then
    APP=$APP-$1
fi

PROCESS_TYPE=web
REGISTRY=registry.heroku.com
TAG=$REGISTRY/$APP/$PROCESS_TYPE

docker login --username=_ --password=$HEROKU_API_KEY $REGISTRY
docker build -f docker/prod.Dockerfile -t $TAG .
docker push $TAG
docker rmi $(docker images $TAG -q)
heroku container:release $PROCESS_TYPE -a $APP

heroku run python manage.py migrate -a $APP
