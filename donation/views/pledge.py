from __future__ import absolute_import

import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import transaction as django_transaction
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from ipware.ip import get_ip
from redis import StrictRedis
from rratelimit import Limiter

from donation.forms import PledgeForm, PledgeComponentFormSet, PinTransactionForm
from donation.models import PaymentMethod, Receipt
from donation.tasks import send_bank_transfer_instructions_task

r = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
rate_limiter = Limiter(r,
                       action='test_credit_card',
                       limit=settings.CREDIT_CARD_RATE_LIMIT_MAX_TRANSACTIONS,
                       period=settings.CREDIT_CARD_RATE_LIMIT_PERIOD)


def download_receipt(request, pk, secret):
    if request.method != 'GET':
        raise Http404
    try:
        receipt = Receipt.objects.get(pk=pk, secret=secret)
    except Receipt.DoesNotExist:
        return HttpResponseRedirect('/pledge')
    response = HttpResponse(open(receipt.pdf_receipt_location).read(),
                            content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="EAA_Receipt_{0}.pdf"'.format(receipt.pk)
    return response


class PledgeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PledgeView, self).dispatch(request, *args, **kwargs)

    @xframe_options_exempt
    def get(self, request):
        charity = request.GET.get('charity')
        pin_environment = settings.PIN_DEFAULT_ENVIRONMENT
        pin_key = settings.PIN_ENVIRONMENTS[pin_environment].get('key')
        return render(request, 'donation_form.html', {'charity': charity, 'pin_key': pin_key,
                                                      'pin_environment': pin_environment})

    @xframe_options_exempt
    def post(self, request):

        body = json.loads(request.body.decode('utf-8'))
        pledge_form = PledgeForm(body)
        component_formset = PledgeComponentFormSet(body)

        if not (pledge_form.is_valid() and component_formset.is_valid()):
            return JsonResponse({
                'error_message': [pledge_form.errors] + component_formset.errors
            }, status=400)

        with django_transaction.atomic():
            pledge = pledge_form.save()
            for component in component_formset.forms:
                component.instance.pledge = pledge
            component_formset.save()

        response_data = {}

        if pledge.payment_method == PaymentMethod.BANK:
            response_data['bank_reference'] = pledge.generate_reference()
            send_bank_transfer_instructions_task.delay(pledge.id)
            return JsonResponse(response_data)

        elif pledge.payment_method == PaymentMethod.CREDIT_CARD:
            ip = get_ip(request)
            if not rate_limiter.checked_insert(ip) and not settings.DEBUG:
                return JsonResponse({
                    'error_message': "Our apologies: credit card donations are currently unavailable. "
                                     "Please try again tomorrow or make a payment by bank transfer.",
                }, status=400)

            pin_data = body.get('pin_response')
            pin_data['amount'] = pledge.amount
            pin_data['pledge'] = pledge.id
            pin_form = PinTransactionForm(pin_data)
            if not pin_form.is_valid():
                return JsonResponse({
                    'error_message': pin_form.errors
                }, status=400)

            transaction = pin_form.save()
            transaction.process_transaction()
            if transaction.succeeded:
                Receipt.objects.create_from_pin_transaction(transaction)
                response_data['succeeded'] = True
                receipt = transaction.receipt_set.first()
                response_data['receipt_url'] = reverse('download-receipt',
                                                       kwargs={'pk': receipt.pk, 'secret': receipt.secret})
                return JsonResponse(response_data)
            else:
                return JsonResponse({
                    'error_message': transaction.pin_response_text,
                }, status=400)

        else:
            raise StandardError('We currently only support new donations via credit card or bank transfer.')
