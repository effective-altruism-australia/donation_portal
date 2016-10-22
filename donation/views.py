from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import TransitionalDonationsFileUploadForm


@login_required()
def upload_donations_file(request):
    if request.method == 'POST':
        form = TransitionalDonationsFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/admin/donation/pledge/')
    else:
        form = TransitionalDonationsFileUploadForm()
    return render(request, 'transitional_upload_form.html', {'form': form})
