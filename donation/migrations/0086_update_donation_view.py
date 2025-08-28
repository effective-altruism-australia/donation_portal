# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0085_auto_20210103_1112"),
    ]

    operations = [
        migrations.RunSQL(
            """
    DROP VIEW IF EXISTS donation_donation CASCADE;

    CREATE VIEW donation_donation AS
      (SELECT id AS id,
              TIMEZONE('LIGT', "date"::TIMESTAMP) + '18 hours' AS "datetime",
              "date",
              amount,
              0 AS fees,
              'Bank transfer' AS payment_method,
              "reference",
              pledge_id,
              id AS bank_transaction_id,
              NULL::int AS pin_transaction_id,
              NULL::int AS stripe_transaction_id
       FROM donation_banktransaction WHERE do_not_reconcile = FALSE AND PLEDGE_ID IS NOT NULL) UNION
       (SELECT 10000000 + id AS id,
              TIMEZONE('LIGT', "date"::TIMESTAMP) AS "datetime",
              "date",
              amount,
              0 AS fees,
              'Stripe' AS payment_method,
              "reference",
              pledge_id,
              NULL::int AS bank_transaction_id,
              NULL::int AS pin_transaction_id,
              id AS stripe_transaction_id
       FROM donation_stripetransaction where PLEDGE_ID IS NOT NULL) UNION
      (SELECT 1000000 + id AS id,
              "date" AS "datetime",
              ("date" AT TIME ZONE 'LIGT')::date AS "date",
              amount,
              fees,
              'Credit card' AS payment_method,
              transaction_token AS "reference",
              pledge_id,
              NULL::int AS bank_transaction_id,
              id AS pin_transaction_id,
              NULL::int AS stripe_transaction_id
       FROM pinpayments_pintransaction A JOIN donation_pintransaction B ON (A.id = B.pintransaction_ptr_id)
       WHERE processed=TRUE AND succeeded=TRUE);
    """
        )
    ]
