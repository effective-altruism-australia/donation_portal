from __future__ import unicode_literals

import json

from django.db import models


class PartnerCharity(models.Model):
    slug_id = models.CharField(max_length=30, unique=True, null=True)
    name = models.TextField(unique=True, verbose_name='Name (human readable)')
    email = models.EmailField(help_text="Used to cc the charity on receipts")
    xero_account_name = models.TextField(help_text="Exact text of incoming donation account in xero")
    active = models.BooleanField(default=True)
    thumbnail = models.CharField(blank=True, null=True, max_length=100)

    order = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name

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
        super(PartnerCharity, self).save(*args, **kwargs)
        PartnerCharity.cache_database_ids()
