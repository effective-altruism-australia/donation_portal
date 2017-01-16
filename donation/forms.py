import arrow

from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import TransitionalDonationsFile


class TransitionalDonationsFileUploadForm(forms.ModelForm):
    class Meta:
        model = TransitionalDonationsFile
        fields = ['file', ]


class DateRangeSelector(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DateRangeSelector, self).__init__(*args, **kwargs)
        years = range(2015, arrow.now().year + 1)
        start_of_month = arrow.now().replace(months=-1).replace(day=1).date()
        end_of_month = arrow.now().replace(day=1).replace(days=-1).date()
        self.fields['start'].widget.years = years
        self.fields['start'].initial = start_of_month
        self.fields['end'].widget.years = years
        self.fields['end'].initial = end_of_month

    start = forms.DateField(widget=SelectDateWidget(), label='Start date')
    end = forms.DateField(widget=SelectDateWidget(), label='End date')
