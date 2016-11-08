import arrow

from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import TransitionalDonationsFile


class TransitionalDonationsFileUploadForm(forms.ModelForm):
    class Meta:
        model = TransitionalDonationsFile
        fields = ['file', ]


class DateRangeSelector(forms.Form):
    years = range(2015, arrow.now().date().year + 1)

    # Probably we want the last complete month to be the default ?
    start_of_month = arrow.now().replace(months=-1).replace(day=1).date()
    end_of_month = arrow.now().replace(day=1).replace(days=-1).date()

    start = forms.DateField(widget=SelectDateWidget(years=years), label='Start date', initial=start_of_month)
    end = forms.DateField(widget=SelectDateWidget(years=years), label='End date', initial=end_of_month)
