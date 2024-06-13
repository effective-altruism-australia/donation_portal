# Payment backend for Effective Altruism Australia

## Configuration

Configuration is via [salt](https://docs.saltstack.com/en/latest/) but we haven't open-sourced the salt pillar and
states yet. We'll eventually open source these and add a setup script that makes getting a dev instance up and running automatic.

In the meantime, it's pretty much a vanilla django/celery app that shouldn't be too hard to get working.
Here are some notes that may help:

1. We use Ubuntu 16.04.
2. Packages required are in https://github.com/effective-altruism-australia/donation_portal/blob/live/deps. The list of
pip packages is complete but the list of apt packages is incomplete, missing things like redis and postgres that salt
installs separately.
3. Settings are split between https://github.com/effective-altruism-australia/donation_portal/blob/live/donation_portal/settings.py
and https://github.com/effective-altruism-australia/donation_portal/blob/live/donation_portal/salt_settings_example.py.

## Example data

To add some example data: `./manage.py loaddata example-data`