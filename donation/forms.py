import arrow

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import ChoiceInput

from .models import TransitionalDonationsFile, Pledge, PartnerCharity


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


class PledgeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PledgeForm, self).__init__(*args, **kwargs)
        self.fields['recipient_org'].queryset = PartnerCharity.objects.filter(
            show_on_website=True,
        )

    class Meta:
        model = Pledge
        fields = ['amount', 'first_name', 'last_name', 'email', 'subscribe_to_updates',
                  'how_did_you_hear_about_us', 'payment_method', 'recipient_org', 'recurring']


    class Media:
        js = ('js/pledge.js', 'js/process_steps.js', 'js/credit_card.js')
        css = {'all': ('css/pledge.css', 'css/process_steps.css', 'css/credit_card.css')}


    # These values control the donation amount buttons shown
    donation_amounts = (('$100', 100),
                        ('$250', 250),
                        ('$500', 500),
                        ('$1000', 1000),
                        )

    # The template will display labels for these fields
    show_labels = ['amount', 'how_did_you_hear_about_us']

    partner_charities = PartnerCharity.objects.filter(show_on_website=True)

