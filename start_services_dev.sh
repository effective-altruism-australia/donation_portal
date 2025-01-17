#!/bin/bash

# Start the virtual environment
source donation_portal_env/bin/activate

# Run stripe webhook listener
echo "**************************************************************"
echo "* If testing Stripe locally, remember run:                   *"
echo "* stripe listen --forward-to localhost:8000/stripe-webhooks/ *"
echo "**************************************************************"

# Start PostgreSQL service
sudo service postgresql start

# Start Redis service
sudo service redis-server start

# Start celery
celery -A donation_portal worker --beat -l INFO &

# Apply database migrations
python manage.py migrate

# Run the Django development server
python manage.py runserver 0.0.0.0:8000