#!/bin/bash

set -e

chmod +x /wait
/wait

python manage.py runserver 0:80
