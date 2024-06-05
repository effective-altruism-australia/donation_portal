#!/bin/bash

# Run commands as user 'eaa' without an interactive shell
sudo -u eaa -H bash << EOF

echo "Logged in successfully."

# Navigate to the project directory
cd /home/eaa/donation_portal/react

# Pull the latest changes from the repository
git pull

echo "Building frontend."
npm run build

cd /home/eaa/donation_portal

workon donation_portal

echo "Collecting staticfiles."
./manage.py collectstatic

echo "Migrating db."
./manage.py migrate

EOF

echo "Restarting service."
sudo supervisorctl restart donations:

echo "Deployment completed successfully."