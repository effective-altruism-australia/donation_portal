from __future__ import absolute_import

from django.db.models import F
from django.http.response import JsonResponse
from django.views.generic import View

from donation.models import PartnerCharity, ReferralSource
from django.views.generic.base import TemplateView
from django.views.decorators.clickjacking import xframe_options_exempt


class ImpactCalculator(TemplateView):

    template_name = "impact.html"

    @xframe_options_exempt
    def get(self, request):
        return super(ImpactCalculator, self).get(request)