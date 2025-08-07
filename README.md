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

## Notes on choices:
1. Chose to host on Azure because we get $2k USD/year as a NFP
2. Chose managed Postgres so that we don't need to deal with updates or security patches
3. Chose to use public end points with IP restricted access for Postgres as the speed and security costs vs an internal endpoint are negligible while the benefit of making it available to (e.g. Retool) is large
4. Considered app services and a containerised app rather than a VM but realised it would be more complicated than it's worth due to needing separate Redis, Celery and storage services. It's also easier from a debugging perspective if all the services (aside from the db) are on the same machine.
