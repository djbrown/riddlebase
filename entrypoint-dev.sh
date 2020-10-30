#!/bin/sh

export DJANGO_SETTINGS_MODULE="riddlebase.settings"
./manage.py migrate
./manage.py collectstatic --no-input

uvicorn --reload --host 0.0.0.0 --port 8000 riddlebase.asgi:application
# ./manage.py runserver 0.0.0.0:8000
