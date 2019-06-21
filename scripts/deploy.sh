#!/bin/bash

set -e

APP=tv-tracker
TAG=$DOCKER_USERNAME/$APP

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
sudo docker build -f docker/production/Dockerfile -t $TAG .
docker push $TAG

sudo pip install awscli

INSTANCE_ID=$(sudo aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=hobby-infra" "Name=tag:Env,Values=production" \
    --query "Reservations[0].Instances[0].InstanceId" \
    --output text)

sudo aws ssm send-command \
    --instance-ids $INSTANCE_ID \
    --document-name "AWS-RunShellScript" \
    --parameters commands=["cd /apps/$APP/ && sh app_init.sh"]
