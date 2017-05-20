from __future__ import absolute_import

import os
from collections import OrderedDict
from datetime import datetime, date

import xlsxwriter
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render
from enumfields import Enum

from donation.models import Donation


@login_required()
def render_export_page(request):
    return render(request, 'export.html')


@login_required()
def download_spreadsheet(request, extra_fields=None):
    # TODO We don't pass parameters to this function yet.
    # Write some javascript to restrict dates. Maybe easiest to switch out the date widgets for the jQuery UI ones.
    if request.method != 'GET':
        raise Http404

    if extra_fields is None:
        extra_fields = []

    try:
        start = datetime.strptime(request.GET['start'], '%Y-%m-%d').date()
    except (KeyError, ValueError):
        start = date(2016, 1, 1)

    try:
        end = datetime.strptime(request.GET['end'], '%Y-%m-%d').date()
    except (KeyError, ValueError):
        end = date.today()

    path = os.path.join(settings.MEDIA_ROOT, 'downloads')
    filename = 'EAA donations {0} to {1} downloaded {2}.xlsx'.format(start, end, datetime.now())
    with xlsxwriter.Workbook(os.path.join(path, filename)) as wb:
        ws = wb.add_worksheet()
        date_format = wb.add_format({'num_format': 'dd mmm yyyy'})
        template = OrderedDict([
            ('Date', 'date'),
            ('Amount', 'amount'),
            ('EAA Reference', 'reference'),
            ('First Name', 'pledge__first_name'),
            ('Last Name', 'pledge__last_name'),
            ('Email', 'pledge__email'),
            ('Payment method', 'payment_method'),
            ('Subscribe to marketing updates', 'pledge__subscribe_to_updates'),
            ('Can publish donation', 'pledge__publish_donation'),
            ('Designation', 'pledge__recipient_org__name')
        ] + extra_fields)
        ws.write_row(0, 0, template.keys())
        row = 0
        for bt_row in Donation.objects. \
                filter(date__gte=start, date__lte=end). \
                order_by('date'). \
                values_list(*template.values()):
            row += 1
            # Resolve any Enums
            bt_row = [value.label if isinstance(value, Enum) else value for value in bt_row]
            ws.write_datetime(row, 0, bt_row[0].replace(tzinfo=None), date_format)
            ws.write_row(row, 1, bt_row[1:])

    response = HttpResponse(open(os.path.join(path, filename)).read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response


@login_required()
def download_full_spreadsheet(request):
    # TODO add credit card donation details (e.g., address), to the extent we have them
    extra_fields = [
        ('Fees', 'pin_transaction__fees'),
        ('Recurring donor', 'pledge__recurring'),
        ('Recurring frequency', 'pledge__recurring_frequency'),
        ('How did you hear about us?', 'pledge__how_did_you_hear_about_us'),
        ('Share with GiveWell', 'pledge__share_with_givewell'),
        ('Share with GWWC', 'pledge__share_with_gwwc'),
        ('Share with TLYCS', 'pledge__share_with_tlycs'),
    ]
    return download_spreadsheet(request, extra_fields)
