#!/bin/bash

# Run stripe webhook listener
echo "**************************************************************"
echo "* If testing Stripe locally, remember run:                   *"
echo "* stripe listen --forward-to localhost:8000/stripe-webhooks/ *"
echo "**************************************************************"

# Start PostgreSQL service
# sudo service postgresql start

# Memcached
# sudo service memcached start

# Start Redis service
# sudo service redis-server start

# Start celery (kill existing workers first)
pkill -f "celery.*donation_portal" || true
PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig" DYLD_LIBRARY_PATH="/opt/homebrew/lib" uv run celery -A donation_portal worker --beat -l INFO &

# Wait for celery to start
echo "Waiting for Celery to start..."
sleep 3

# Collect static files
uv run manage.py collectstatic --noinput

# Apply database migrations
uv run manage.py migrate

# Run the Django development server
uv run manage.py runserver 0.0.0.0:8000