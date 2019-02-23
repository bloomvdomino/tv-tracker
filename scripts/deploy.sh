#!/bin/bash

set -e

echo "$HEROKU_AUTH_TOKEN" | docker login -u _ --password-stdin registry.heroku.com
docker build -f docker/prod.Dockerfile -t registry.heroku.com/"$HEROKU_APP_NAME"/web .
docker push registry.heroku.com/"$HEROKU_APP_NAME"/web
