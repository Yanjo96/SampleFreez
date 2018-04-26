#!/bin/bash

sudo

#install requirements
pip install django
pip install django-widget-tweaks
pip install django-multiselectfield
pip install django-bootstrap4

#make files
SECRET_KEY="secretkey = '"$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)"'"
echo $SECRET_KEY > samplefreez/settings_secret.py

#Einrichten
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

python manage.py shell < database_settings.py






