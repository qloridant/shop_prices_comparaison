#!/bin/bash

# Post compile
export PYTHONPATH=/build/${REQUEST_ID}/.apt/usr/lib/python3/dist-packages/:${PYTHONPATH}
python manage.py collectstatic --noinput

# Post deploy
python manage.py migrate

# Start
gunicorn open_shop_compare.wsgi --log-file -


