from __future__ import absolute_import

from django.db.models import F
from django.http.response import JsonResponse
from django.views.generic import View

from donation.models import PartnerCharity, ReferralSource
from django.views.generic.base import TemplateView


class ImpactCalculator(TemplateView):

    template_name = "impact.html"
