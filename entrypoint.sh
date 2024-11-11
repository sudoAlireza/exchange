#!/bin/bash

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py spectacular --color --file schema.yml

gunicorn core.wsgi:application  --bind 0:8000 --workers 3

exec "$@"