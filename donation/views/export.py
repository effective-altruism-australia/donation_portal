from __future__ import absolute_import

import os
from collections import OrderedDict
from datetime import datetime, date


import xlsxwriter
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from enumfields import Enum

from donation.models import Donation
import string
import random

def generate_random_string(length=10):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


@login_required()
def render_export_page(request):
    return render(request, 'export.html')


@login_required()
def download_spreadsheet(request, extra_fields=None):
    # TODO We don't pass date parameters to this function yet.
    # Write some javascript to restrict dates. Maybe easiest to switch out the date widgets for the jQuery UI ones.
    if request.method != 'GET':
        raise Http404

    try:
        start = datetime.strptime(request.GET['start'], '%Y-%m-%d').date()
    except (KeyError, ValueError):
        start = date(2016, 1, 1)

    try:
        end = datetime.strptime(request.GET['end'], '%Y-%m-%d').date()
    except (KeyError, ValueError):
        end = date.today()

    if extra_fields is None:
        extra_fields = []
    template = OrderedDict([
                               ('Date', 'datetime'),
                               ('Amount', 'components__amount'),
                               ('EAA Reference', 'reference'),
                               ('First Name', 'pledge__first_name'),
                               ('Last Name', 'pledge__last_name'),
                               ('Email', 'pledge__email'),
                               ('Payment method', 'payment_method'),
                               ('Subscribe to marketing updates', 'pledge__subscribe_to_updates'),
                               ('Designation', 'components__pledge_component__partner_charity__name'),
                               ('Recurring donor', 'pledge__recurring'),
                               ('Recurring frequency', 'pledge__recurring_frequency')
                           ] + extra_fields)

    filename = 'EAA_donations_{0}.xlsx'.format(str(date.today()))
    location = os.path.join("/tmp", filename)
    if not os.path.exists(location):
        # Note that the values call below is required to create a donation object for each associated pledge component
        queryset = Donation.objects.filter(date__gte=start, date__lte=end).order_by('datetime')
        donation_ids = list(queryset.values_list('id', flat=True))
        from donation.tasks import export_spreadsheet
        export_spreadsheet.delay(location, donation_ids, template)
        return HttpResponse("Please wait 5 minutes and refresh this page again.")
    else:
        response = HttpResponse(open(location).read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response


def write_spreadsheet(location, donations, template, cleaned=False):
    with xlsxwriter.Workbook(location, {'default_date_format': 'dd mmm yyyy'}) as wb:
        for name, donation in donations.items():
            ws = wb.add_worksheet(name=name)
            ws.write_row(0, 0, template.keys())
            row_number = 0
            for row in donation.values_list(*template.values()):
                if cleaned:
                    row_list = list(row)
                    if not row_list[9]:
                        row_list[5] = "anonymous"
                        row_list[6] = "anonymous"
                        row_list[7] = "anonymous"    
                    row = tuple(row_list)
                row_number += 1
                # Resolve any Enums
                row = [value.label if isinstance(value, Enum) else value for value in row]
                # Excel can't cope with time zones
                row = [value.astimezone(timezone.get_default_timezone()).replace(tzinfo=None)
                       if isinstance(value, datetime) else value for value in row]
                ws.write_row(row_number, 0, row)


@login_required()
def download_full_spreadsheet(request):
    # TODO add credit card donation details (e.g., address), to the extent we have them
    extra_fields = [
        ('Fees', 'components__fees'),
        ('How did you hear about us?', 'pledge__how_did_you_hear_about_us_db__reason'),
        ('Share with GiveWell', 'pledge__share_with_givewell'),
        ('Share with GWWC', 'pledge__share_with_gwwc'),
        ('Share with TLYCS', 'pledge__share_with_tlycs'),
        ('Gift', 'pledge__is_gift'),
    ]
    return download_spreadsheet(request, extra_fields)
