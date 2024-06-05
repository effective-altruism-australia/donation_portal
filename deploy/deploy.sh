#!/bin/bash
sudo -u eaa -H -i

# Navigate to the project directory
cd /home/eaa/donation_portal

# Pull the latest changes from the repository
git pull

echo "Deployment completed successfully."
