#!/bin/bash

# Start PostgreSQL service
sudo service postgresql start

# Start Redis service
sudo service redis-server start

# Start celery
celery -A donation_portal worker -l info

# Apply database migrations
python manage.py migrate

# Run the Django development server
python manage.py runserver 0.0.0.0:8000
