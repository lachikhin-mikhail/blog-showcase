#!/bin/bash

docker exec -it blog-django python3 manage.py makemigrations

docker exec -it blog-django python3 manage.py migrate
