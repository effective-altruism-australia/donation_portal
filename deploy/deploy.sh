#!/bin/bash

# Run commands as user 'eaa' without an interactive shell
sudo -u eaa -H bash << EOF

echo "Logged in successfully."

# Navigate to the project directory
cd /home/eaa/donation_portal

# Pull the latest changes from the repository
git pull

echo "Deployment completed successfully."

EOF
