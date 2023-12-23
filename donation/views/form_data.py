from __future__ import absolute_import

from django.db.models import F
from django.http.response import JsonResponse
from django.views.generic import View

from donation.models import PartnerCharity, ReferralSource


class PartnerCharityView(View):
    def get(self, request):
        charity_names = PartnerCharity.objects.filter(active=True).order_by('ordering').values('slug_id', 'name',
                                                                                            'thumbnail', "category",
                                                                                            "is_eaae")
        
        # If url params containes "eaae", then filter for eaae charities
        if request.GET.get('eaae'):
            charity_names = charity_names.filter(is_eaae=True)
        else:
            charity_names = charity_names.filter(is_eaae=False)
        return JsonResponse(list(charity_names), safe=False)


class ReferralSourceView(View):
    def get(self, request):
        referral_sources = ReferralSource.objects.filter(
            enabled=True).order_by('order').annotate(value=F('slug_id'), label=F('reason')).values('value', 'label')
        return JsonResponse(list(referral_sources), safe=False)
