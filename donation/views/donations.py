from __future__ import absolute_import

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import View
from ipware.ip import get_ip
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings

from donation.forms import PledgeForm
from donation.models import Receipt, RecurringFrequency, PinTransaction, PartnerCharity

from redis import StrictRedis
from rratelimit import Limiter

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


# TODO It's weird these are combined since one is JSON and one is not
class PledgeView(View):
    @xframe_options_exempt
    def post(self, request):
        form = PledgeForm(request.POST)

        if form.is_valid():
            form.save()
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
            pledge.send_bank_transfer_instructions()
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
            transaction.amount = form.cleaned_data['amount']  # Amount in dollars. Define with your own business logic.
            transaction.currency = 'AUD'  # Pin supports AUD and USD. Fees apply for currency conversion.
            transaction.description = 'Donation to Effective Altruism Australia'  # Define with your own business logic
            transaction.email_address = pledge.email
            transaction.pledge = pledge
            transaction.save()
            transaction.process_transaction()  # Typically "Success" or an error message
            if transaction.succeeded:
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
        paypal_dict = {
            "business": "placeholder@example.com",
            "amount": "0",
            "item_name": "Donation",
            "notify_url": "https://www.example.com" + reverse('paypal-ipn'),
            "return_url": "https://www.example.com/your-return-location/",
            "cancel_return": "https://www.example.com/your-cancel-location/",
        }
        paypal_form = PayPalPaymentsForm(button_type='donate', initial=paypal_dict)
        form = PledgeForm()

        return render(request, 'pledge.html', {
            'form': form,
            'paypal_form': paypal_form,
            'charity_database_ids': PartnerCharity.get_cached_database_ids(),
            })
