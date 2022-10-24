#!/bin/bash
docker-compose kill back

docker rm blog-django
docker volume rm blog-showcase_blog-django

docker-compose up -d --build

docker exec -it blog-django python3 manage.py makemigrations
docker exec -it blog-django python3 manage.py migrate

echo -en "\007"
