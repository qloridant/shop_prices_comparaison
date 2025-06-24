#!/bin/bash

python manage.py migrate
gunicorn open_shop_compare.wsgi --log-file -


