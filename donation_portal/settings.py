"""
Django settings for donation_portal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import datetime
from celery.schedules import crontab

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
    'pinpayments',
    'reversion',
    'donation',
    'captcha',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
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
TIME_ZONE = 'UTC'
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

# Celery
# http://docs.celeryproject.org/en/latest/configuration.html

# To run Celery: celery -A donation_portal worker --beat -l INFO

# We'll run this every 4 hours in case xero is late importing transactions or something
CELERYBEAT_SCHEDULE = {
    'process-transactions': {
        'task': 'donation.tasks.process_bank_transactions',
        'schedule': crontab(minute=0, hour='*/4')
        # 'schedule': datetime.timedelta(seconds=30)  # For testing
    },
}

LOGIN_URL = '/admin/login'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Deployment

# Settings configured by Salt
if os.path.exists(os.path.join(os.path.dirname(__file__), "salt_settings.py")):
    # noinspection PyUnresolvedReferences
    from salt_settings import *  # NOQA
else:
    from salt_settings_example import *  # NOQA

# Custom configuration settings
if os.path.exists(os.path.join(os.path.dirname(__file__), "local_settings.py")):
    # noinspection PyUnresolvedReferences
    from local_settings import *  # NOQA

if ENABLE_SENTRY:
    INSTALLED_APPS += ('raven.contrib.django.raven_compat', )

# Date from which to start sending receipts automatically (inclusive)
AUTOMATION_START_DATE = datetime.date(2016, 10, 19)

# vim: cc=80 tw=79 ts=4 sw=4 sts=4 et sr
