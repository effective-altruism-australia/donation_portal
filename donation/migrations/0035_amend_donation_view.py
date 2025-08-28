# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0034_auto_20170630_0743"),
    ]

    operations = [
        migrations.RunSQL(
            """
    DROP VIEW IF EXISTS donation_donation;

    CREATE VIEW donation_donation AS
      (SELECT id AS id,
              TIMEZONE('LIGT', "date"::TIMESTAMP) + '18 hours' AS "datetime",
              "date",
              amount,
              'Bank transfer' AS payment_method,
              "reference",
              pledge_id,
              id AS bank_transaction_id,
              NULL::int AS pin_transaction_id
       FROM donation_banktransaction WHERE do_not_reconcile = FALSE AND PLEDGE_ID IS NOT NULL) UNION
      (SELECT 1000000 + id AS id,
              "date" AS "datetime",
              ("date" AT TIME ZONE 'LIGT')::date AS "date",
              amount,
              'Credit card' AS payment_method,
              transaction_token AS "reference",
              pledge_id,
              NULL::int AS bank_transaction_id,
              id AS pin_transaction_id
       FROM pinpayments_pintransaction A JOIN donation_pintransaction B ON (A.id = B.pintransaction_ptr_id)
       WHERE processed=TRUE AND succeeded=TRUE);
    """
        )
    ]
