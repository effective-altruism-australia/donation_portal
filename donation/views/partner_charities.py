from __future__ import absolute_import

from django.core import serializers
from django.http.response import JsonResponse, HttpResponse
from django.views.generic import View

from donation.models import PartnerCharity


class PartnerCharityView(View):
    def get(self, request):

        charity_names = PartnerCharity.objects.order_by('order')
        data = serializers.serialize('json', list(charity_names), fields=('slug_id', 'name'))
        return HttpResponse(data)
