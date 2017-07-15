import arrow
import datetime
import os
from collections import OrderedDict

from django.conf import settings
from django.db.models import Max, Q
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from django.utils import timezone

from raven.contrib.django.raven_compat.models import client

from donation.models import PartnerCharity, PartnerCharityReport, Donation
from donation.views.export import write_spreadsheet


def send_partner_charity_reports(test=True):
    # Create list of partners, combined the GiveDirectly entries
    partners = {partner.name: [partner.id] for partner in PartnerCharity.objects.all()}
    partners['GiveDirectly'] += partners['GiveDirectly Basic income research']
    del partners['GiveDirectly Basic income research']

    for partner, ids in partners.iteritems():
        # Start time is when we last reported
        last_report_datetime = PartnerCharityReport.objects.filter(partner__id=ids[0]).aggregate(Max('date'))['date__max'] or datetime.datetime(2016, 1, 1, 0, 0, 0)
        start = arrow.get(last_report_datetime).datetime
        # End date is midnight yesterday (i.e. midnight between yesterday and today) UTC
        # It could be the current time too (or rather a minute ago, to avoid races).
        end = arrow.get(arrow.utcnow().date()).datetime

        # Create spreadsheet
        querysets = OrderedDict([
            ('New donations',
             # For bank transactions, we use time_reconciled
             Donation.objects.filter(Q(bank_transaction__bank_account_id=settings.XERO_INCOMING_ACCOUNT_ID,
                                       # Keep Westpac transactions out until we finish reconciling them
                                       bank_transaction__time_reconciled__gte=start,
                                       bank_transaction__time_reconciled__lt=end) |
                                     Q(pin_transaction__isnull=False,
                                       datetime__gte=start,
                                       datetime__lt=end),
                                     pledge__recipient_org__id__in=ids).order_by('datetime')),
            ('All donations',
             Donation.objects.filter(Q(bank_transaction__bank_account_id=settings.XERO_INCOMING_ACCOUNT_ID,
                                       # Keep Westpac transactions out until we finish reconciling them
                                       bank_transaction__time_reconciled__lt=end) |
                                     Q(pin_transaction__isnull=False,
                                       datetime__lt=end),
                                     pledge__recipient_org__id__in=ids).order_by('datetime'))])

        template = OrderedDict([
                                   ('Date', 'datetime'),
                                   ('Amount', 'amount'),
                                   ('Fees', 'pin_transaction__fees'),
                                   ('EAA Reference', 'reference'),
                                   ('First Name', 'pledge__first_name'),
                                   ('Last Name', 'pledge__last_name'),
                                   ('Email', 'pledge__email'),
                                   ('Payment method', 'payment_method'),
                                   ('Subscribe to marketing updates', 'pledge__subscribe_to_updates'),
                                   ('Designation', 'pledge__recipient_org__name')
                               ])

        filename = 'EAA donation report - {0} - {1}.xlsx'.format(partner,
                                                                 # Avoid collisions of filename while testing
                                                                 timezone.now())
        location = os.path.join(settings.MEDIA_ROOT, 'partner_reports', filename)

        write_spreadsheet(location, querysets, template)

        # Create email
        try:
            partner_email = PartnerCharity.objects.get(id=ids[0]).email
            body = render_to_string('partner_report_message.txt', {'name': partner})
            message = EmailMessage(
                subject='Effective Altruism Australia donation report',
                body=body,
                to=[partner_email] if not test else ['ben.toner@eaa.org.au'],
                cc=['info@eaa.org.au', 'ben.toner@eaa.org.au'] if not test else ['ben.toner@eaa.org.au'],
                # There is a filter in info@eaa.org.au
                #   from:(donations @ eaa.org.au) deliveredto:(info + receipts @ eaa.org.au)
                # that automatically archives messages sent to info+receipt and adds the label 'receipts'
                # bcc=["info+receipt@eaa.org.au", ],
                bcc=[],
                from_email=settings.POSTMARK_SENDER,
            )
            message.attach_file(location, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            get_connection().send_messages([message])
        except Exception as e:
            client.captureException()

        if not test:
            partner = PartnerCharity.objects.get(id=ids[0])
            PartnerCharityReport(partner=partner, date=end).save()
