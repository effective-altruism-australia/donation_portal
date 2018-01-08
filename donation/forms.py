import arrow
import os

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import ChoiceInput
from django.conf import settings

from .models import TransitionalDonationsFile, Pledge, PartnerCharity, ReferralSource


class TransitionalDonationsFileUploadForm(forms.ModelForm):
    class Meta:
        model = TransitionalDonationsFile
        fields = ['file', ]


class DateRangeSelector(forms.Form):
    def __init__(self, *args, **kwargs):
        last_month = kwargs.pop('last_month', False)
        super(DateRangeSelector, self).__init__(*args, **kwargs)

        years = range(2016, arrow.now().year + 1)
        if last_month:
            start_date = arrow.now().replace(months=-1).replace(day=1).date()
            end_date = arrow.now().replace(day=1).replace(days=-1).date()
        else:
            start_date = arrow.Arrow(2016, 1, 1).date()
            end_date = arrow.now().date()
        self.fields['start'].widget.years = years
        self.fields['start'].initial = start_date
        self.fields['end'].widget.years = years
        self.fields['end'].initial = end_date

    start = forms.DateField(widget=SelectDateWidget(), label='Start date')
    end = forms.DateField(widget=SelectDateWidget(), label='End date')


class PledgeForm(forms.ModelForm):
    class Meta:
        model = Pledge
        fields = ['amount', 'first_name', 'email', 'how_did_you_hear_about_us_db', 'subscribe_to_updates',
                  'payment_method', 'recipient_org', 'recurring']

    class Media:
        # Don't use Media as it's compatible with ManifestStaticFilesStorage on Django 1.8
        # https://code.djangoproject.com/ticket/21221
        pass

    # These values control the donation amount buttons shown
    donation_amounts_raw = (25, 50, 100, 250)
    donation_amounts = [('$' + str(x), x) for x in donation_amounts_raw]

    referral_sources = ReferralSource.objects.filter(enabled=True).order_by('order')

    # The template will display labels for these fields
    hide_labels = ['subscribe_to_updates', ]
