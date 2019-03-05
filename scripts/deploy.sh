#!/bin/bash

# https://devcenter.heroku.com/articles/container-registry-and-runtime

set -e

heroku_app_name=api-tv-tracker
process_type=web
tag=registry.heroku.com/$heroku_app_name/$process_type

docker build -f docker/prod.Dockerfile -t $tag .
docker push $tag
heroku container:release $process_type
docker rmi $(docker images $tag -q)

heroku run python manage.py migrate
