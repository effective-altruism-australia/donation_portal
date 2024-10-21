"""
Django settings for donation_portal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import datetime
import os

from celery.schedules import crontab
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Helper function to get environment variables with defaults and casting
def get_env(name, default=None, cast=str):
    value = os.environ.get(name, default)
    if value is None:
        return None
    
    if cast == bool:
        return value.lower() in ('true', 't', 'yes', 'y', '1')
    
    try:
        return cast(value)
    except ValueError:
        return default

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrap3',
    'corsheaders',
    'pinpayments',
    'reversion',
    'donation.apps.DonationConfig',
    'paypal.standard.ipn',
    'webpack_loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'donation_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'donation_portal.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-au'
TIME_ZONE = 'Australia/Melbourne'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "tmp/static")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Celery
# http://docs.celeryproject.org/en/latest/configuration.html
# To run Celery: celery -A donation_portal worker --beat -l INFO
# We'll run this every 4 hours in case xero is late importing transactions or something
CELERYBEAT_SCHEDULE = {
    'process-transactions': {
        'task': 'donation.tasks.process_bank_transactions',
        # 'schedule': datetime.timedelta(seconds=30)  # For testing
        'schedule': crontab(minute=0, hour='3')
    },
    'import-trial-balance': {
        'task': 'donation.tasks.import_trial_balance',
        # 'schedule': datetime.timedelta(seconds=30)  # For testing
        'schedule': crontab(minute=0, hour='15')
    },
    'send-partner-charity-reports': {
        'task': 'donation.tasks.send_partner_charity_reports_task',
        'schedule': crontab(minute=0, hour=5, day_of_week='1')
    }
}
BROKER_URL = 'redis://localhost:6379'

# Redis
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'

LOGIN_URL = '/admin/login'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CREDIT_CARD_RATE_LIMIT_MAX_TRANSACTIONS = 6
CREDIT_CARD_RATE_LIMIT_PERIOD = 12 * 60 * 60
CREDIT_CARD_RATE_LIMIT_ENABLED = True

TESTING_EMAIL = get_env('TESTING_EMAIL')
EAA_INFO_EMAIL = 'info@eaa.org.au'

# Debug mode (do *not* set to True in production)
DEBUG = get_env('DEBUG', False, bool)

# Secret key used to provide cryptographic signing
SECRET_KEY = get_env('SECRET_KEY')

# Security settings
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = get_env('CSRF_COOKIE_SECURE', True, bool)
SESSION_COOKIE_SECURE = get_env('SESSION_COOKIE_SECURE', True, bool)
CORS_ORIGIN_WHITELIST = os.environ.get('CORS_ORIGIN_WHITELIST', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env('POSTGRES_DB_NAME'),
        'USER': get_env('POSTGRES_USER'),
        'PASSWORD': get_env('POSTGRES_PASSWORD'),
        'HOST': get_env('POSTGRES_HOST'),
        'PORT': get_env('POSTGRES_PORT'),
    }
}

# Email (Postmark)
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
POSTMARK_API_KEY = get_env('POSTMARK_API_KEY')
POSTMARK_SENDER = get_env('POSTMARK_SENDER')
POSTMARK_TEST_MODE = get_env('POSTMARK_TEST_MODE', False, bool)
POSTMARK_TRACK_OPENS = get_env('POSTMARK_TRACK_OPENS', False, bool)

# Email (MailChimp)
MAILCHIMP_API_KEY = get_env('MAILCHIMP_API_KEY')
EA_NEWSLETTER_MAILCHIMP_API_KEY = get_env('EA_NEWSLETTER_MAILCHIMP_API_KEY')

# Xero
XERO_RSA_KEY = get_env('XERO_RSA_KEY')
XERO_CONSUMER_KEY = get_env('XERO_CONSUMER_KEY')
XERO_INCOMING_ACCOUNT_ID_DICT = {
    "eaa": get_env('XERO_INCOMING_ACCOUNT_ID_EAA'), 
    "eaae": get_env('XERO_INCOMING_ACCOUNT_ID_EAAE')
}
XERO_INCOMING_ACCOUNT_ID = get_env('XERO_INCOMING_ACCOUNT_ID_EAA')
XERO_DAYS_TO_IMPORT = 300
XERO_CLIENT_ID = get_env('XERO_CLIENT_ID')
XERO_CLIENT_SECRET = get_env('XERO_CLIENT_SECRET')
TENANT_IDS = {
    'eaa': get_env('XERO_TENANT_ID_EAA'),
    'eaae': get_env('XERO_TENANT_ID_EAAE')
}

# Stripe
STRIPE_API_KEY = get_env('STRIPE_API_KEY_EAA')
STRIPE_API_KEY_DICT = {
    "eaa": get_env('STRIPE_API_KEY_EAA'), 
    "eaae": get_env('STRIPE_API_KEY_EAAE')
}

# Pinpayments
PIN_ENVIRONMENTS = {"No longer used"}

# Sentry
ENABLE_SENTRY = get_env('ENABLE_SENTRY', True, bool)

if ENABLE_SENTRY:
    INSTALLED_APPS += ('raven.contrib.django.raven_compat',)
    import raven
    release = None
    try:
        release = raven.fetch_git_sha(os.path.dirname(__file__))
    except:
        pass

    SENTRY_DSN = get_env('SENTRY_DSN')
    SENTRY_PUBLIC_DSN = get_env('SENTRY_PUBLIC_DSN')
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
        'release': release
    }
SENTRY_PUBLIC_DSN = get_env('SENTRY_PUBLIC_DSN')

# Date from which to start sending receipts automatically (inclusive)
AUTOMATION_START_DATE = datetime.date(2016, 10, 19)

# Webpack
STATICFILES_DIRS = STATICFILES_DIRS + (
    os.path.join(BASE_DIR, 'react', 'build'),
    os.path.join(BASE_DIR, 'react', 'public'),
)
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundle/',
        'STATS_FILE': os.path.join(BASE_DIR, 'react/build/webpack-stats.json'),
        # This disables polling in production. We assume the bundles are built and stay unchanged while the application is running.
        'CACHE': not DEBUG,
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60 * 60 * 60 * 24,
        'OPTIONS': {
            'MAX_ENTRIES': 5000,
        }
    }
}