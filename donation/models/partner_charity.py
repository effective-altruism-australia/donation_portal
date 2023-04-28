from __future__ import unicode_literals

import json

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
import stripe
from django.conf import settings

stripe.api_version = "2020-08-27"


def validate_impact_text(impact_text):
    if impact_text.count('{0}') == 0:
        raise ValidationError(
            _('The impact text must contain "{0}" where the impact size will be inserted.'),
        )


class PartnerCharity(models.Model):
    slug_id = models.CharField(max_length=30, unique=True, null=True)
    name = models.TextField(unique=True, verbose_name='Name (human readable)')
    email = models.EmailField(help_text="Used to send the partner charity reports")
    email_cc = models.EmailField(null=True, blank=True, help_text="Cced on partner charity reports")
    xero_account_name = models.TextField(help_text="Exact text of incoming donation account in xero")
    active = models.BooleanField(default=True)
    thumbnail = models.CharField(blank=True, null=True, max_length=100)

    bio = models.TextField(blank=True)
    website = models.CharField(null=True, blank=True, max_length=200)

    category = models.CharField(null=True, blank=True, max_length=50, choices=((x, x) for x in ("Our recommended charities", "Other charities we support", "Help us do more good")))

    impact_text = models.CharField(blank=True, null=True, max_length=500, validators=[validate_impact_text])
    impact_cost = models.FloatField(blank=True, null=True, help_text='Total impact will be calculated as donation '
                                                                     'amount divided by impact cost')
    ordering = models.IntegerField(default=1)

    stripe_product_id = models.CharField(null=True, blank=True, max_length=100)

    is_eaae = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
        
    @property
    def bsb(self):
        return "083004" if self.is_eaae else "083170"
        
    @property
    def account_number(self):
        return "931587719" if self.is_eaae else "306556167"

    class Meta:
        verbose_name_plural = "Partner charities"

    _cached_database_ids = None

    @classmethod
    def cache_database_ids(cls):
        cls._cached_database_ids = json.dumps({x['name']: x['id'] for x in cls.objects.all().values('name', 'id')})

    @classmethod
    def get_cached_database_ids(cls):
        if not cls._cached_database_ids:
            cls.cache_database_ids()
        return cls._cached_database_ids

    def save(self, *args, **kwargs):
        if not self.stripe_product_id:
            stripe.api_key = settings.STRIPE_API_KEY_DICT.get("eaae" if self.is_eaae else "eaa")
            self.stripe_product_id =  stripe.Product.create(name=self.name).id
        super(PartnerCharity, self).save(*args, **kwargs)
        PartnerCharity.cache_database_ids()

    def impact_str(self, amount):
        if self.impact_cost and self.impact_text:
            impact_size = int(float(amount) / self.impact_cost)
            return self.impact_text.format(impact_size)
