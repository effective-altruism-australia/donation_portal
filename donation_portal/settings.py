import datetime
import os
import logging

from dotenv import load_dotenv
from celery.schedules import crontab
import sentry_sdk

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

##################
## Django setup ##
##################

# Do NOT set to "True" in production
DEBUG = os.getenv("DEBUG").lower() == "true"

SECRET_KEY = os.getenv("SECRET_KEY")

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "corsheaders",
    "pinpayments",
    "reversion",
    "donation.apps.DonationConfig",
    "paypal.standard.ipn",
)

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": ColoredFormatter,
            "format": "{levelname} {asctime} [{module}:{lineno}] {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "file": {
            "format": "{levelname} {asctime} [{module}:{lineno}] {funcName} - {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "django.log",
            "maxBytes": 10 * 1024 * 1024,  # 10MB
            "backupCount": 5,
            "formatter": "file",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "django.db.backends": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

WSGI_APPLICATION = "donation_portal.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
EMAIL_BACKEND = "postmark.django_backend.EmailBackend"

ENABLE_DEBUG_TOOLBAR = DEBUG

if ENABLE_DEBUG_TOOLBAR and DEBUG:
    INSTALLED_APPS += ("debug_toolbar",)
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]


if os.getenv("USE_SENTRY").lower() == "true":
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
    )

# Internationalization
LANGUAGE_CODE = "en-au"
TIME_ZONE = "Australia/Melbourne"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# URLs
ROOT_URLCONF = "donation_portal.urls"
LOGIN_URL = "/admin/login"
STATIC_URL = "/static/"
STATIC_ROOT = os.getenv("STATIC_ROOT")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
CORS_ORIGIN_WHITELIST = [
    "https://staging.effectivealtruism.org.au",
    "https://donations.effectivealtruism.org.au",
    "https://effectivealtruism.org.au",
    "http://localhost:8000",
    "http://localhost:8001",
]
ALLOWED_HOSTS = [
    "effectivealtruism.org.au",
    "staging.effectivealtruism.org.au",
    "donations.effectivealtruism.org.au",
    "localhost",
]
CSRF_TRUSTED_ORIGINS = [
    "https://effectivealtruism.org.au",
    "https://staging.effectivealtruism.org.au",
    "https://donations.effectivealtruism.org.au",
]

BASE_URL = os.getenv("ORIGIN")


############
## Celery ##
############

# We'll run this every 4 hours in case xero is late importing transactions or something
CELERYBEAT_SCHEDULE = {
    "process-transactions": {
        "task": "donation.tasks.process_bank_transactions",
        # 'schedule': datetime.timedelta(seconds=30)  # For testing
        "schedule": crontab(minute=0, hour="3"),
    },
    "import-trial-balance": {
        "task": "donation.tasks.import_trial_balance",
        # 'schedule': datetime.timedelta(seconds=30)  # For testing
        "schedule": crontab(minute=0, hour="15"),
    },
    "send-partner-charity-reports": {
        "task": "donation.tasks.send_partner_charity_reports_task",
        "schedule": crontab(minute=0, hour=5, day_of_week="1"),
    },
}
BROKER_CONNECTION_RETRY_ON_STARTUP = True
BROKER_URL = os.getenv("REDIS_URL")
CELERY_BROKER_URL = os.getenv("REDIS_URL")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL")
CELERY_TASK_ALWAYS_EAGER = DEBUG
CELERY_TASK_EAGER_PROPAGATES = DEBUG
CREDIT_CARD_RATE_LIMIT_MAX_TRANSACTIONS = 6
CREDIT_CARD_RATE_LIMIT_PERIOD = 12 * 60 * 60
CREDIT_CARD_RATE_LIMIT_ENABLED = True


##############
## Postgres ##
##############

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("PGDATABASE"),
        "USER": os.getenv("PGUSER"),
        "PASSWORD": os.getenv("PGPASSWORD"),
        "HOST": os.getenv("PGHOST"),
        "PORT": os.getenv("PGPORT"),
        "OPTIONS": {
            "sslmode": os.getenv("PGSSLMODE"),
        },
        "DISABLE_SERVER_SIDE_CURSORS": True,
    }
}


###########
## Redis ##
###########

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_USE_SSL = os.getenv("REDIS_USE_SSL").lower() == "true"


############
## Stripe ##
############

STRIPE_API_KEY_DICT = {
    "eaa": os.getenv("STRIPE_SECRET_KEY_EAA"),
    "eaae": os.getenv("STRIPE_SECRET_KEY_EAAE"),
}


##########
## Xero ##
##########

XERO_DAYS_TO_IMPORT = 300
XERO_CALLBACK_URI = f"{BASE_URL}/process_callback"
XERO_RSA_KEY = os.getenv("XERO_RSA_KEY")
XERO_CONSUMER_KEY = os.getenv("XERO_CONSUMER_KEY")
XERO_CLIENT_ID = os.getenv("XERO_CLIENT_ID")
XERO_CLIENT_SECRET = os.getenv("XERO_CLIENT_SECRET")
XERO_INCOMING_ACCOUNT_ID_DICT = {
    "eaa": os.getenv("XERO_INCOMING_ACCOUNT_ID_EAA"),
    "eaae": os.getenv("XERO_INCOMING_ACCOUNT_ID_EAAE"),
}
TENANT_IDS = {
    "eaa": os.getenv("TENANT_ID_EAA"),
    "eaae": os.getenv("TENANT_ID_EAAE"),
}


###############
## Memcached ##
###############

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
        "TIMEOUT": 60 * 60 * 60 * 24,  # 24 hours
        "OPTIONS": {},
    }
}


###########
## Email ##
###########

TESTING_EMAIL = os.getenv("TESTING_EMAIL")
EAA_INFO_EMAIL = os.getenv("TESTING_EMAIL") if DEBUG else "info@eaa.org.au"
POSTMARK_SENDER = "donations@eaa.org.au"
POSTMARK_API_KEY = os.getenv("POSTMARK_API_KEY")
MAILCHIMP_API_KEY = os.getenv("MAILCHIMP_API_KEY")
EA_NEWSLETTER_MAILCHIMP_API_KEY = os.getenv("EA_NEWSLETTER_MAILCHIMP_API_KEY")


###########
## Misc. ##
###########

# Directory where various secrets are stored (e.g. RSA keys)
SECRETS_DIR = os.path.join(BASE_DIR, "secrets")

# Use custom test runner to enforce system checks before tests
TEST_RUNNER = "donation.test_runner.SystemCheckTestRunner"

# Date from which to start sending receipts automatically (inclusive)
AUTOMATION_START_DATE = datetime.date(2016, 10, 19)

# We're not using this anymore but we'l kept it for stability (just in case)
PIN_ENVIRONMENTS = {"dummy"}
