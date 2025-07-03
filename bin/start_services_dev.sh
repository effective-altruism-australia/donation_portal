#!/bin/bash

# Start the virtual environment
source .venv/bin/activate

# Run stripe webhook listener
echo "**************************************************************"
echo "* If testing Stripe locally, remember run:                   *"
echo "* stripe listen --forward-to localhost:8000/stripe-webhooks/ *"
echo "**************************************************************"

# Start PostgreSQL service
sudo service postgresql start

# Memcached
sudo service memcached start

# Start Redis service
sudo service redis-server start

# Start celery
celery -A donation_portal worker --beat -l INFO &

# Collect static files
./manage.py collectstatic --noinput

# Apply database migrations
uv run manage.py migrate

# Run the Django development server
uv run manage.py runserver 0.0.0.0:8000