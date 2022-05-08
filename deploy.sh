#!/bin/sh     
sudo git pull origin master
sudo pip3 install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic -n
sudo systemctl restart nginx
sudo systemctl restart uwsgi