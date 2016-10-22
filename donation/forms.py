from django.forms import ModelForm

from .models import TransitionalDonationsFile


class TransitionalDonationsFileUploadForm(ModelForm):
    class Meta:
        model = TransitionalDonationsFile
        fields = ['file', ]
