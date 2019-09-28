#!/bin/bash

set -e

/wait
python manage.py runserver 0:8000
