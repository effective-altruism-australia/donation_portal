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

    filename = 'EAA donations {0} to {1} downloaded {2}.xlsx'.format(start, end, datetime.now())
    location = os.path.join(settings.STATIC_ROOT, filename)

    # Note that the values call below is required to create a donation object for each associated pledge component
    queryset = Donation.objects.values('components').filter(
        date__gte=start, date__lte=end).order_by('datetime')
    write_spreadsheet(location, {'Donations': queryset}, template)

    response = HttpResponse("https://donations.effectivealtruism.com.au/static/" + filename)
    return response


def write_spreadsheet(location, querysets, template):
    with xlsxwriter.Workbook(location, {'default_date_format': 'dd mmm yyyy'}) as wb:
        for name, queryset in querysets.iteritems():
            ws = wb.add_worksheet(name=name)
            ws.write_row(0, 0, template.keys())
            row_number = 0
            for row in queryset.values_list(*template.values()):
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
    ]
    return download_spreadsheet(request, extra_fields)
