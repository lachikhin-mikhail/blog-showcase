#!/bin/bash
docker-compose kill back
docker-compose kill nginx

docker rm blog-django
docker rm blog-nginx
docker volume rm blog-showcase_blog-django
docker volume rm blog-showcase_blog-static

docker-compose up -d --build

docker exec -it blog-django python3 manage.py collectstatic <<<yes
docker exec -it blog-django python3 manage.py migrate
docker exec -it blog-django python3 manage.py makemigrations

docker exec -it blog-django python3 manage.py migrate

echo -en "\007"
