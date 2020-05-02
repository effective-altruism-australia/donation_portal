from __future__ import absolute_import

import datetime
import json
import os
import time

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
from raven.contrib.django.raven_compat.models import client
from redis import StrictRedis
from rratelimit import Limiter

from donation.forms import PledgeForm, PledgeComponentFormSet, PinTransactionForm, PledgeFormOld
from donation.models import PaymentMethod, Receipt, PartnerCharity, PinTransaction, RecurringFrequency
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


class PledgeJS(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PledgeJS, self).dispatch(request, *args, **kwargs)

    @xframe_options_exempt
    def get(self, request):
        with open(os.path.join(settings.BASE_DIR, 'react/build/webpack-stats.json')) as f:
            data = json.load(f)

        time_last_compiled = datetime.datetime.utcfromtimestamp(data['endTime'] / 1000)
        time_last_compiled.timetuple()

        url = data['chunks']['donation_form'][0]['publicPath']

        response = HttpResponseRedirect(url, content_type="application/x-javascript")
        response['Last-Modified'] = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time_last_compiled.timetuple())
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
            client.captureMessage(str(pledge_form.errors) + str(component_formset.errors), data=body)
            return JsonResponse({
                'error_message': "There was a problem submitting your donation. Please contact info@eaa.org.au if problems persist."
            }, status=400)

        total = sum([component.instance.amount for component in component_formset.forms])
        if total < 2:
            return JsonResponse({
                'error_message': "The minimum donation possible is $2.",
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
            if not rate_limiter.checked_insert(ip) and not settings.DEBUG and settings.CREDIT_CARD_RATE_LIMIT_ENABLED:
                client.captureMessage('Hit rate limiter for ip: %s' % ip)
                return JsonResponse({
                    'error_message': "Our apologies: credit card donations are currently unavailable. "
                                     "Please try again tomorrow or make a payment by bank transfer.",
                }, status=400)

            if pledge.amount > 6000:
                client.captureMessage('User attempted credit card donation over $6K')
                return JsonResponse({
                    'error_message': "Our apologies: we can only accept credit card donations of up to $6000 AUD.  "
                                     "Please use bank transfer or make multiple smaller donations.",
                }, status=400)

            pin_data = body.get('pin_response')
            pin_data['amount'] = pledge.amount
            pin_data['pledge'] = pledge.id
            pin_form = PinTransactionForm(pin_data)
            if not pin_form.is_valid():
                client.captureMessage(str(pin_form.errors))
                return JsonResponse({
                    'error_message': "There was a problem submitting your donation. Please contact info@eaa.org.au if problems persist."
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
                pin_repsonse_dict = json.loads(transaction.pin_response_text)
                client.captureMessage(pin_repsonse_dict['error_description'])
                return JsonResponse({
                    'error_message': "There was a problem submitting your donation. Please contact info@eaa.org.au if problems persist.",
                }, status=400)

        else:
            raise StandardError('We currently only support new donations via credit card or bank transfer.')


class PledgeViewOld(View):
    @xframe_options_exempt
    def post(self, request):
        form = PledgeFormOld(request.POST)
        amount = request.POST.get('amount')
        partner_id = request.POST.get('recipient_org')
        partner_slug = PartnerCharity.objects.get(id=partner_id).slug_id
        components_data = {'form-TOTAL_FORMS': 1, 'form-INITIAL_FORMS': 1, 'form-0-id': None,
                           'form-0-amount': amount, 'form-0-partner_charity': partner_slug}
        component_formset = PledgeComponentFormSet(components_data)

        if form.is_valid() and component_formset.is_valid():
            pledge = form.save()
            for component in component_formset.forms:
                component.instance.pledge = pledge
            component_formset.save()
        else:
            return JsonResponse({
                'error': 'form-error',
                'form_errors': form.errors
            }, status=400)

        pledge = form.instance
        if pledge.recurring:
            pledge.recurring_frequency = RecurringFrequency.MONTHLY
            pledge.save()
        payment_method = request.POST.get('payment_method')
        response_data = {'payment_method': payment_method}

        if int(payment_method) == 1:
            # bank transaction
            response_data['bank_reference'] = pledge.generate_reference()
            send_bank_transfer_instructions_task.delay(pledge.id)
            return JsonResponse(response_data)
        elif int(payment_method) == 3:
            # Rate limiting
            ip = get_ip(request)
            if not rate_limiter.checked_insert(ip):
                # Pretend it's a PIN error to save us from handling it separately in the javascript.
                return JsonResponse({
                    'error': 'pin-error',
                    'pin_response': "Our apologies: credit card donations are currently unavailable. " +
                                    "Please try again tomorrow or make a payment by bank transfer.",
                    'pin_response_text': '',
                }, status=400)

            transaction = PinTransaction()
            transaction.card_token = request.POST.get('card_token')
            transaction.ip_address = request.POST.get('ip_address')
            transaction.amount = pledge.amount  # Amount in dollars. Define with your own business logic.
            transaction.currency = 'AUD'  # Pin supports AUD and USD. Fees apply for currency conversion.
            transaction.description = 'Donation to Effective Altruism Australia'  # Define with your own business logic
            transaction.email_address = pledge.email
            transaction.pledge = pledge
            transaction.save()
            transaction.process_transaction()  # Typically "Success" or an error message
            if transaction.succeeded:
                Receipt.objects.create_from_pin_transaction(transaction)
                response_data['succeeded'] = True
                receipt = transaction.receipt_set.first()
                response_data['receipt_url'] = reverse('download-receipt',
                                                       kwargs={'pk': receipt.pk, 'secret': receipt.secret})
                return JsonResponse(response_data)
            else:
                return JsonResponse({
                    'error': 'pin-error',
                    'pin_response': transaction.pin_response,
                    'pin_response_text': transaction.pin_response_text,
                }, status=400)

    @xframe_options_exempt
    def get(self, request):

        form = PledgeFormOld()

        return render(request, 'pledge.html', {
            'form': form,
            'charity_database_ids': PartnerCharity.get_cached_database_ids(),
        })
