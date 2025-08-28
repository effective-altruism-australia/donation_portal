"""
System checks for external dependencies (DB, cache, Redis, Celery, API keys).
"""

from django.core.checks import register, Error, Warning
from django.db import connections
from django.core.cache import caches
from django.conf import settings

import stripe
from redis import StrictRedis
from redis.exceptions import RedisError


@register()
def check_database_connection(app_configs, **kwargs):
    """Verify database connectivity."""
    errors = []
    try:
        connections["default"].cursor()
    except Exception as e:
        errors.append(
            Error(
                f"Database connection failed: {e}",
                id="donation.E001",
            )
        )
    return errors


@register()
def check_redis_connection(app_configs, **kwargs):
    """Verify Redis is accessible for rate limiting and Celery broker."""
    errors = []
    try:
        r = StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            username=settings.REDIS_USERNAME,
            password=settings.REDIS_PASSWORD,
            db=0,
            ssl=settings.REDIS_USE_SSL,
        )
        r.ping()
        print("Redis connection successful.")
    except RedisError as e:
        errors.append(
            Error(
                f"Redis connection failed: {e}",
                id="donation.E002",
            )
        )
    return errors


@register()
def check_cache_backend(app_configs, **kwargs):
    """Verify default cache (e.g. Memcached) is writable/readable."""
    errors = []
    try:
        cache = caches["default"]
        cache.set("_health_check", "ok", timeout=5)
        if cache.get("_health_check") != "ok":
            errors.append(
                Error(
                    "Cache read/write failed.",
                    id="donation.E003",
                )
            )
    except Exception as e:
        errors.append(
            Error(
                f"Cache access failed: {e}",
                id="donation.E004",
            )
        )
    return errors


@register()
def check_stripe_api_keys(app_configs, **kwargs):
    """Ensure Stripe API keys are configured."""
    errors = []
    keys = getattr(settings, "STRIPE_API_KEY_DICT", None)
    if not isinstance(keys, dict) or not keys:
        errors.append(
            Error(
                "Missing STRIPE_API_KEY_DICT configuration.",
                id="donation.E005",
            )
        )
    else:
        for org, key in keys.items():
            if not key:
                errors.append(
                    Error(f"Empty Stripe API key for '{org}'.", id="donation.E006")
                )
    return errors


@register()
def check_mailchimp_api_key(app_configs, **kwargs):
    """Ensure Mailchimp API key is set."""
    errors = []
    if not getattr(settings, "MAILCHIMP_API_KEY", None):
        errors.append(
            Error(
                "Missing MAILCHIMP_API_KEY configuration.",
                id="donation.E007",
            )
        )
    return errors


@register()
def check_xero_configuration(app_configs, **kwargs):
    """Ensure Xero integration settings are present."""
    errors = []
    for var in ("XERO_CLIENT_ID", "XERO_CLIENT_SECRET"):
        if not getattr(settings, var, None):
            errors.append(
                Error(
                    f"Missing {var} in settings.",
                    id="donation.E008",
                )
            )
    tenants = getattr(settings, "TENANT_IDS", None)
    if not isinstance(tenants, dict) or not tenants:
        errors.append(
            Error(
                "Missing TENANT_IDS configuration for Xero tenants.",
                id="donation.E009",
            )
        )
    return errors


@register()
def check_celery_workers(app_configs, **kwargs):
    """Warn if no Celery workers are responsive."""
    from donation_portal.eaacelery import app as celery_app

    errors = []
    try:
        insp = celery_app.control.inspect(timeout=1)
        ping = insp.ping()
        if not ping:
            errors.append(
                Warning(
                    "No running Celery workers detected.",
                    id="donation.W001",
                )
            )
    except Exception:
        errors.append(
            Warning(
                "Unable to ping Celery workers.",
                id="donation.W002",
            )
        )
    return errors
