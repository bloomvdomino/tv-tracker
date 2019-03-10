#!/bin/bash

# https://devcenter.heroku.com/articles/container-registry-and-runtime

set -e

heroku_app=my-tv-tracker
process_type=web
tag=registry.heroku.com/$heroku_app/$process_type

docker build -f docker/prod.Dockerfile -t $tag .
docker push $tag
heroku container:release -a $heroku_app $process_type
docker rmi $(docker images $tag -q)

heroku run -a $heroku_app python manage.py migrate
