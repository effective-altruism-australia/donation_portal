import arrow
import os

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import ChoiceInput
from django.conf import settings

from .models import Pledge, PartnerCharity, ReferralSource


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
