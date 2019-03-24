#!/bin/bash

# Update system packages.
sudo apt-get update -y
sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold"

# Install Docker and Docker Compose.
sudo apt-get install -y docker.io
sudo curl \
    -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Pull Docker images and start services.
sudo docker-compose -f ${docker_compose_base} -f ${docker_compose_production} -p ${project} up -d
sudo docker exec ${project}_web_1 python manage.py collectstatic --noinput --clear
sudo docker exec ${project}_web_1 python manage.py migrate
