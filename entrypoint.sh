#!/bin/bash

python manage.py collectstatic --noinput

gunicorn jobtracker.wsgi:application --bind 0.0.0.0:8000