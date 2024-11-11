#!/bin/sh

# Execute structure migrations
python manage.py migrate main
python manage.py migrate
