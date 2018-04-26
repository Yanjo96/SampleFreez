#!/bin/bash

sudo

#install requirements
pip install django
pip install django-widget-tweaks
pip install django-multiselectfield
pip install django-bootstrap4

#make files
SECRET_KEY="secretkey = '"$(cat /dev/urandom | tr -dc 'a-zA-Z0-9!@#$%^&*(_=+)-' | fold -w 50 | head -n 1)"'"
echo $SECRET_KEY > samplefreez/settings_secret.py

#set up database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

TYPES=('Citrat' 'EDTA' 'Lithium Heparin' 'Serum' 'Natriumcitrat' 'Natriumfluorid' 'Paxgene')
touch database_settings.py

echo "from sample.models import Type" >> database_settings.py

for i in ${TYPES[@]}; do
  LINE='Type.objects.create(name='$i')'
  echo $LINE >> database_settings.py
done

python manage.py shell < database_settings.py
rm database_settings.py





