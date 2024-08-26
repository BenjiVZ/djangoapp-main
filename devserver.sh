#!/bin/sh
source .venv/bin/activate
python manage.py runserver $PORT
python manage.py runserver 8001
