import arrow
import datetime

from collections import OrderedDict

from django.db.models import Max
from django.utils import timezone

from donation.models import *
from donation.views.export import write_spreadsheet


def send_partner_charity_reports(test=True):
    # Create list of partners, combined the GiveDirectly entries
    # TODO: respect the "test" parameter
    partners = {partner.name: [partner.id] for partner in PartnerCharity.objects.all()}
    partners['GiveDirectly'] += partners['GiveDirectly Basic income research']
    del partners['GiveDirectly Basic income research']

    for partner, ids in partners.iteritems():
        # Start date is day after we last reported
        last_report_date = PartnerCharityReport.objects.filter(partner__id=ids[0]).aggregate(Max('date'))['date__max'] or datetime.date(2016, 1, 1)
        start = arrow.get(last_report_date).replace(days=+1).datetime
        # End date is yesterday (for completeness)
        end = arrow.get(datetime.date.today()).replace(days=-1).datetime

        # Create spreadsheet
        querysets = OrderedDict([
            ('New donations', Donation.objects.filter(date__gte=start,
                                                      date__lte=end,
                                                      pledge__recipient_org__id__in=ids).order_by('date')
                              # include donations that weren't reconciled until later
                              | Donation.objects.filter(bank_transaction__time_reconciled__gte=start,
                                                        date__lte=end,
                                                        pledge__recipient_org__id__in=ids).order_by('date')),
            ('All donations', Donation.objects.filter(date__lte=end,
                                                      pledge__recipient_org__id__in=ids).order_by('date'))])

        template = OrderedDict([
                                   ('Date', 'date'),
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

        filename = 'EAA donation report - {0} - {1}.xlsx'.format(partner, timezone.now())
        location = os.path.join(settings.MEDIA_ROOT, 'partner_reports', filename)

        write_spreadsheet(location, querysets, template)

        # Create email
        try:
            body = render_to_string('partner_report_message.txt', {'name': partner})
            message = EmailMessage(
                subject='Effective Altruism Australia donation report',
                body=body,
                to=['ben.toner@eaa.org.au'],
                cc=[],
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
