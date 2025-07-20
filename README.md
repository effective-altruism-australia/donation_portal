# Payment backend for Effective Altruism Australia

## System Dependencies
* [uv](https://docs.astral.sh/uv)
* weasyprint
* pango
* glib
* cairo
* gobject-introspection
* gdk-pixbuf
* libffi

## Services
* Postgres
* Redis
* Memcache
* Celery

## API Keys
* Mailchimp
* Postmark
* Stripe
* Xero (+ Account IDs)

## Development
You have a few options for setting up a development environment.

### Development Frontend
* `uv sync` to create a virtual environment and install dependencies
* `uv run frontend/dev.py` to start a dev server with auto-rebuilds upon changes in `./src`
Note: the donation form needs to make API calls to get the list of charity partners and referral sources. You can set the `ORIGIN` in `.env` to be `donations.effectivealtruism.org.au` or `localhost:8000` depending on whether you want to use the live production values or the local Django values.

### Development Backend
* Run the `docker-compose` file to set up backing services like Redis, Postgres and memcache.
* `uv sync` to create a virtual environment and install dependencies
* `source bin/apply_patches.sh` to patch old dependencies
* `uv run manage.py runserver` to start the Django server

## Notes on choices:
1. Chose Azure because we get $2k USD/year as a NFP
2. Chose managed Postgres so that we don't need to deal with updates or security patches
3. Chose to make it publicly available as the speed and security costs are negligible while the benefit of making it available to e.g. retool or dashboarding tools is large
4. Considered app services and a containerised app rather than a VM but realised it would be more complicated than its worth due to needing redis and celery (would have to run as separate app services) and permanent storage of media (extra overhead in a addition to running the vm). It's also easier from a debugging perspective if all the services (aside from the db) are on the same machine.
