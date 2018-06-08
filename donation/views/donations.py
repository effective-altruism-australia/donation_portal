from __future__ import absolute_import

import json
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import transaction as django_transaction
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import View
from ipware.ip import get_ip
from redis import StrictRedis
from rratelimit import Limiter

from django.views.decorators.csrf import csrf_exempt

from donation import emails
from donation.forms import PledgeForm, PledgeComponentFormSet, PinTransactionForm
from donation.models import Receipt, PinTransaction, PaymentMethod, Receipt
from donation.tasks import send_bank_transfer_instructions_task
from django.conf import settings


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


class PledgeViewNew(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PledgeViewNew, self).dispatch(request, *args, **kwargs)

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
                'error': 'form-error',
                'form_errors': [pledge_form.errors] + component_formset.errors
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
            pin_data = body.get('pin_response')
            pin_data['amount'] = pledge.amount_from_components
            pin_data['pledge'] = pledge.id
            pin_form = PinTransactionForm(pin_data)
            if not pin_form.is_valid():
                return JsonResponse({
                    'error': 'form-error',
                    'form_errors': pin_form.errors
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
                    'error': 'pin-error',
                    'pin_response': transaction.pin_response,
                    'pin_response_text': transaction.pin_response_text,
                }, status=400)

        else:
            raise StandardError('We currently only support new donations via credit card or bank transfer.')


# TODO It's weird these are combined since one is JSON and one is not
class PledgeView(View):
    @xframe_options_exempt
    def post(self, request):
        pass
        # form = PledgeForm(request.POST)
        #
        # if form.is_valid():
        #     form.save()
        # else:
        #     return JsonResponse({
        #         'error': 'form-error',
        #         'form_errors': form.errors
        #     }, status=400)
        #
        # pledge = form.instance
        # if pledge.recurring:
        #     pledge.recurring_frequency = RecurringFrequency.MONTHLY
        #     pledge.save()
        # payment_method = request.POST.get('payment_method')
        # response_data = {'payment_method': payment_method}
        #
        # if int(payment_method) == 1:
        #     # bank transaction
        #     response_data['bank_reference'] = pledge.generate_reference()
        #     emails.send_bank_transfer_instructions(pledge)
        #     return JsonResponse(response_data)
        # elif int(payment_method) == 3:
        # Rate limiting
        # ip = get_ip(request)
        # if not rate_limiter.checked_insert(ip):
        #     # Pretend it's a PIN error to save us from handling it separately in the javascript.
        #     return JsonResponse({
        #         'error': 'pin-error',
        #         'pin_response': "Our apologies: credit card donations are currently unavailable. " +
        #                         "Please try again tomorrow or make a payment by bank transfer.",
        #         'pin_response_text': '',
        #     }, status=400)
        #
        # transaction = PinTransaction()
        # transaction.card_token = request.POST.get('card_token')
        # transaction.ip_address = request.POST.get('ip_address')
        # transaction.amount = form.cleaned_data['amount']  # Amount in dollars. Define with your own business logic.
        # transaction.currency = 'AUD'  # Pin supports AUD and USD. Fees apply for currency conversion.
        # transaction.description = 'Donation to Effective Altruism Australia'  # Define with your own business logic
        # transaction.email_address = pledge.email
        # transaction.pledge = pledge
        # transaction.save()
        # transaction.process_transaction()  # Typically "Success" or an error message
        # if transaction.succeeded:
        #     response_data['succeeded'] = True
        #     receipt = transaction.receipt_set.first()
        #     response_data['receipt_url'] = reverse('download-receipt',
        #                                            kwargs={'pk': receipt.pk, 'secret': receipt.secret})
        #     return JsonResponse(response_data)
        # else:
        #     return JsonResponse({
        #         'error': 'pin-error',
        #         'pin_response': transaction.pin_response,
        #         'pin_response_text': transaction.pin_response_text,
        #     }, status=400)

    # @xframe_options_exempt
    def get(self, request):
        pass
        # paypal_dict = {
        #     "business": "placeholder@example.com",
        #     "amount": "0",
        #     "item_name": "Donation",
        #     "notify_url": "https://www.example.com" + reverse('paypal-ipn'),
        #     "return_url": "https://www.example.com/your-return-location/",
        #     "cancel_return": "https://www.example.com/your-cancel-location/",
        # }
        # paypal_form = PayPalPaymentsForm(button_type='donate', initial=paypal_dict)
        # form = PledgeForm()
        #
        # return render(request, 'pledge.html', {
        #     'form': form,
        #     'paypal_form': paypal_form,
        #     'charity_database_ids': PartnerCharity.get_cached_database_ids(),
        #     })
