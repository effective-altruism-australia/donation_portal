import arrow
from django import forms
from django.forms.widgets import SelectDateWidget
from enumfields.fields import EnumChoiceField

from donation.models import RecurringFrequency, Pledge, ReferralSource, PaymentMethod, PartnerCharity, PledgeComponent, \
    PinTransaction


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


class PaymentMethodField(EnumChoiceField):
    def clean(self, value):
        mapping_dict = {
            'bank-transfer': PaymentMethod.BANK,
            'credit-card': PaymentMethod.CREDIT_CARD,
        }
        return mapping_dict[value]


class RecurringFrequencyField(EnumChoiceField):
    def clean(self, value):
        # Currently the donation form only supports a monthly (or once off) donation frequency
        mapping_dict = {
            'one-time': None,
            'monthly': RecurringFrequency.MONTHLY
        }
        return mapping_dict[value]


class PledgeForm(forms.ModelForm):
    class Meta:
        model = Pledge
        fields = ['first_name', 'last_name', 'email', 'how_did_you_hear_about_us_db', 'subscribe_to_updates',
                  'payment_method', 'recurring', 'recurring_frequency', 'is_gift', 'gift_recipient_name',
                  'gift_recipient_email', 'gift_personal_message', 'subscribe_to_newsletter', 'connect_to_community',
                  'postcode', 'country']

    how_did_you_hear_about_us_db = forms.ModelChoiceField(queryset=ReferralSource.objects.all(),
                                                          to_field_name='slug_id', required=False)
    payment_method = PaymentMethodField()
    recurring_frequency = RecurringFrequencyField()

    def __init__(self, *args, **kwargs):
        super(PledgeForm, self).__init__(*args, **kwargs)
        self.referral_sources = ReferralSource.objects.filter(enabled=True).order_by('order')


class PledgeComponentForm(forms.ModelForm):
    class Meta:
        model = PledgeComponent
        fields = ('pledge', 'partner_charity', 'amount')

    partner_charity = forms.ModelChoiceField(queryset=PartnerCharity.objects.all(),
                                             to_field_name='slug_id')
    pledge = forms.ModelChoiceField(queryset=Pledge.objects.all(), required=False)


PledgeComponentFormSet = forms.modelformset_factory(PledgeComponent, form=PledgeComponentForm,
                                                    fields=('pledge', 'partner_charity', 'amount'))


class PinTransactionForm(forms.ModelForm):
    class Meta:
        model = PinTransaction
        fields = '__all__'

    date = forms.DateTimeField(required=False)  # Allow the pin save method to complete this field for us


class PledgeFormOld(forms.ModelForm):
    class Meta:
        model = Pledge
        fields = ['first_name', 'email', 'how_did_you_hear_about_us_db', 'subscribe_to_updates',
                  'payment_method', 'recurring']

    class Media:
        # Don't use Media as it's compatible with ManifestStaticFilesStorage on Django 1.8
        # https://code.djangoproject.com/ticket/21221
        pass

    # These values control the donation amount buttons shown
    donation_amounts_raw = (25, 50, 100, 250)
    donation_amounts = [('$' + str(x), x) for x in donation_amounts_raw]

    # The template will display labels for these fields
    hide_labels = ['subscribe_to_updates', ]

    def __init__(self, *args, **kwargs):
        super(PledgeFormOld, self).__init__(*args, **kwargs)
        self.referral_sources = ReferralSource.objects.filter(enabled=True).order_by('order')
