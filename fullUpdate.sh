#!/bin/bash
docker-compose down -v

docker-compose up -d --build

docker exec -it blog-django python3 manage.py makemigrations

docker exec -it blog-django python3 manage.py migrate


docker exec -it blog-django python3 manage.py collectstatic <<< yes
echo -en "\007"
docker exec -it blog-django python3 manage.py createsuperuser

