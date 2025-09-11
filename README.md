# Payment backend for Effective Altruism Australia

## System Dependencies
* [uv](https://docs.astral.sh/uv)
* weasyprint
* Stripe CLI
* Postgres
* Redis
* Memcached

Note: When developing locally, you can use the `docker-compose.yaml` file to fire up Postgres, Redis and Memcached services. This avoids you having to install them locally.

## API Keys
* Mailchimp
* Postmark
* Stripe
* Xero (+ Account IDs)

## Development

### Development Frontend
* `uv sync` to create a virtual environment and install dependencies
* `uv run frontend/dev.py` to start a dev server with auto-rebuilds upon changes in `./frontend/src`

Note: the donation form needs to make API calls to get the list of charity partners and referral sources. You can set the `ORIGIN` in `.env` to be `donations.effectivealtruism.org.au` or `localhost:8000` depending on whether you want to use the live production values or values from your locally running Django dev server.

### Development Backend
* Run the `docker-compose` file to set up backing services like Redis, Postgres and Memcached.
* `uv sync` to create a virtual environment and install dependencies
* `source bin/apply_patches.sh` to patch old dependencies
* `uv run manage.py runserver` to start the Django dev server

## Production

### Deploying frontend
* Update the `.env` file to use the appropriate production variables
* `uv run frontend/build.py` to build for production
* Copy and paste the output code into a WordPress HTML element

### Deploying backend
* Set up services for Celery beat, Celery workers, Redis, Postgres and Memcached
* Update the `.env` file to use the appropriate production variables
* `uv sync` to create a virtual environment and install dependencies
* `source bin/apply_patches.sh` to patch old dependencies
* Create and run a Gunicorn/Django service

For details consult the "EAA & EAAE Manual".