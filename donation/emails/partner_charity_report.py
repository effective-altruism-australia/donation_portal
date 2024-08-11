import datetime
import os
from collections import OrderedDict

import arrow
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Max, Q
from django.template.loader import render_to_string
from django.utils import timezone
from raven.contrib.django.raven_compat.models import client

from donation.models import PartnerCharity, PartnerCharityReport, Donation
from donation.views.export import write_spreadsheet


def send_partner_charity_reports(test=True):
    # Create list of partners, combined the GiveDirectly entries
    partners = {partner.name: [partner.id] for partner in PartnerCharity.objects.all()}
    if 'GiveDirectly' in partners and 'GiveDirectly Basic income research' in partners:
        partners['GiveDirectly'] += partners['GiveDirectly Basic income research']
        del partners['GiveDirectly Basic income research']

    for partner, ids in partners.iteritems():
        # Start time is when we last reported
        last_report_datetime = PartnerCharityReport.objects.filter(partner__id=ids[0]
                                                                   ).aggregate(Max('date'))[
                                   'date__max'] or datetime.datetime(2016, 1, 1, 0, 0, 0)
        start = arrow.get(last_report_datetime).datetime
        # End date is midnight yesterday (i.e. midnight between yesterday and today) UTC
        # It could be the current time too (or rather a minute ago, to avoid races).
        end = arrow.get(arrow.utcnow().date()).datetime

        # Create spreadsheet
        querysets = OrderedDict(
            [
                (
                    "New donations",
                    # For bank transactions, we use time_reconciled
                    Donation.objects.filter(
                        Q(
                            bank_transaction__time_reconciled__gte=start,
                            bank_transaction__time_reconciled__lt=end,
                        )
                        | Q(
                            pin_transaction__isnull=False,
                            datetime__gte=start,
                            datetime__lt=end,
                        )
                        | Q(
                            stripe_transaction__isnull=False,
                            datetime__gte=start,
                            datetime__lt=end,
                        ),
                        components__pledge_component__partner_charity__id__in=ids,
                    ).order_by("datetime"),
                ),
                (
                    "All donations",
                    Donation.objects.filter(
                        Q(bank_transaction__time_reconciled__lt=end)
                        | Q(pin_transaction__isnull=False, datetime__lt=end)
                        | Q(stripe_transaction__isnull=False, datetime__lt=end),
                        components__pledge_component__partner_charity__id__in=ids,
                    ).order_by("datetime"),
                ),
            ]
        )

        template = OrderedDict([
            ('Date', 'datetime'),
            ('Amount', 'components__amount'),
            ('Fees', 'components__fees'),
            ('Amount (net)', 'components__amount_net'),
            ('EAA Reference', 'reference'),
            ('First Name', 'pledge__first_name'),
            ('Last Name', 'pledge__last_name'),
            ('Email', 'pledge__email'),
            ('Payment method', 'payment_method'),
            ('Subscribe to marketing updates', 'pledge__subscribe_to_updates'),
            ('Designation', 'components__pledge_component__partner_charity__name'),
            ('Recurring (monthly)', 'pledge__recurring'),
            ('Source', 'pledge__how_did_you_hear_about_us_db__reason'),
        ])

        # We add timezone.now() to avoid collisions of filename while testing
        filename = 'EAA donation report - {0} - {1}.xlsx'.format(partner, timezone.now())
        filename_internal = 'EAA donation report - {0} - {1} - internal.xlsx'.format(partner, timezone.now())
        location = os.path.join(settings.MEDIA_ROOT, 'partner_reports', filename)
        location_internal = os.path.join(settings.MEDIA_ROOT, 'partner_reports', filename_internal)

        write_spreadsheet(location, querysets, template, cleaned=True)
        write_spreadsheet(location_internal, querysets, template, cleaned=False)

        # Create email for partner charity (personal information removed)
        try:
            partner_obj = PartnerCharity.objects.get(id=ids[0])
            to = [partner_obj.email]
            cc = [settings.EAA_INFO_EMAIL]

            if partner_obj.email_cc:
                cc.append(partner_obj.email_cc)
            body = render_to_string('partner_report_message.txt', {'name': partner})
            message = EmailMessage(
                subject='Effective Altruism Australia donation report',
                body=body,
                to=to if not test else [settings.TESTING_EMAIL],
                cc=cc if not test else [settings.TESTING_EMAIL],
                # There is a filter in info@eaa.org.au
                #   from:(donations @ eaa.org.au) deliveredto:(info + receipts @ eaa.org.au)
                # that automatically archives messages sent to info+receipt and adds the label 'receipts'
                # bcc=["info+receipt@eaa.org.au", ],
                bcc=[],
                from_email=settings.POSTMARK_SENDER,
            )
            message.attach_file(location, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            message.send()

        except Exception as e:
            print e.message
            client.captureException()

        # Create internal report (personal information included)
        try:
            partner_obj = PartnerCharity.objects.get(id=ids[0])
            to = [settings.EAA_INFO_EMAIL]
            cc = []
            body = "Hi team, here's the internal report for {0} from {1} to {2}".format(partner, start.strftime('%d-%m-%Y'), end.strftime('%d-%m-%Y'))
            message = EmailMessage(
                subject="Internal report for {0} from {1} to {2}".format(partner, start.strftime('%d-%m-%Y'), end.strftime('%d-%m-%Y')),
                body=body,
                to=to if not test else [settings.TESTING_EMAIL],
                cc=cc if not test else [settings.TESTING_EMAIL],
                # There is a filter in info@eaa.org.au
                #   from:(donations @ eaa.org.au) deliveredto:(info + receipts @ eaa.org.au)
                # that automatically archives messages sent to info+receipt and adds the label 'receipts'
                # bcc=["info+receipt@eaa.org.au", ],
                bcc=[],
                from_email=settings.POSTMARK_SENDER,
            )
            message.attach_file(location_internal, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            message.send()

        except Exception as e:
            print e.message
            client.captureException()

        if not test:
            partner = PartnerCharity.objects.get(id=ids[0])
            PartnerCharityReport(partner=partner, date=end).save()
