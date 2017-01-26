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
        last_month = kwargs.pop('last_month', False)
        super(DateRangeSelector, self).__init__(*args, **kwargs)

        years = range(2015, arrow.now().year + 1)
        if last_month:
            start_date = arrow.now().replace(months=-1).replace(day=1).date()
            end_date = arrow.now().replace(day=1).replace(days=-1).date()
        else:
            # TODO when was our first transaction
            start_date = arrow.Arrow(2016, 1, 1).date()
            end_date = arrow.now().date()
        self.fields['start'].widget.years = years
        self.fields['start'].initial = start_date
        self.fields['end'].widget.years = years
        self.fields['end'].initial = end_date

    start = forms.DateField(widget=SelectDateWidget(), label='Start date')
    end = forms.DateField(widget=SelectDateWidget(), label='End date')
