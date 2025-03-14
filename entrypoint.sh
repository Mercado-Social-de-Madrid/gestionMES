#!/bin/sh

echo 'Installing requirements...'
pip install -r requirements.txt

echo 'Running migrations...'
python manage.py migrate

echo 'Compiling SCSS files...'
python manage.py compilescss

echo 'Collecting static files...'
python manage.py collectstatic --no-input

echo 'Starting Django Server...'
exec "$@"