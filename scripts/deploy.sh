#!/bin/bash

set -e

docker login --username=_ --password="$HEROKU_AUTH_TOKEN" registry.heroku.com
docker build -f docker/prod.Dockerfile -t registry.heroku.com/"$HEROKU_APP_NAME"/web .
docker push registry.heroku.com/"$HEROKU_APP_NAME"/web
