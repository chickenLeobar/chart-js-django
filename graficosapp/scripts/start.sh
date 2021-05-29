#!bin/bash
set -e

python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

