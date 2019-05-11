#!/bin/bash

set -e

sudo docker-compose -f ${docker_compose_base} -f ${docker_compose_production} -p ${project} pull
sudo docker-compose -f ${docker_compose_base} -f ${docker_compose_production} -p ${project} up -d

sudo docker exec ${project}_web_1 python manage.py migrate
