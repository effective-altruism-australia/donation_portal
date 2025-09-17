from __future__ import absolute_import

import datetime
import json
import os
import time
import pytz
import stripe
from django.conf import settings
from django.db import transaction as django_transaction
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import View
from donation.models.partner_charity import PartnerCharity
import sentry_sdk
from redis import Redis
from rratelimit import Limiter

from donation.forms import PledgeForm, PledgeComponentFormSet
from donation.models import (
    PaymentMethod,
    Receipt,
    RecurringFrequency,
    Pledge,
    StripeTransaction,
)
from donation.tasks import send_bank_transfer_instructions_task
from donation_portal.eaacelery import app
import logging

logger = logging.getLogger(__name__)
stripe.api_version = "2020-08-27"

r = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    username=settings.REDIS_USERNAME,
    password=settings.REDIS_PASSWORD,
    db=0,
    ssl=settings.REDIS_USE_SSL,
)

rate_limiter = Limiter(
    r,
    action="test_credit_card",
    limit=settings.CREDIT_CARD_RATE_LIMIT_MAX_TRANSACTIONS,
    period=settings.CREDIT_CARD_RATE_LIMIT_PERIOD,
)


def download_receipt(request, pk, secret):
    if request.method != "GET":
        raise Http404
    try:
        receipt = Receipt.objects.get(pk=pk, secret=secret)
    except Receipt.DoesNotExist:
        return HttpResponseRedirect("/pledge")
    response = HttpResponse(
        open(receipt.pdf_receipt_location, "rb").read(), content_type="application/pdf"
    )
    response["Content-Disposition"] = (
        'attachment; filename="EAA_Receipt_{0}.pdf"'.format(receipt.pk)
    )
    return response


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class PledgeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PledgeView, self).dispatch(request, *args, **kwargs)

    @xframe_options_exempt
    def get(self, request):
        charity = request.GET.get("charity")
        return render(request, "donation_form.html", {"charity": charity})

    @xframe_options_exempt
    def post(self, request):
        body = json.loads(request.body.decode("utf-8"))
        pledge_form = PledgeForm(body)
        component_formset = PledgeComponentFormSet(body)

        if not (pledge_form.is_valid() and component_formset.is_valid()):
            sentry_sdk.capture_message(
                str(pledge_form.errors) + str(component_formset.errors), data=body
            )
            return JsonResponse(
                {
                    "error_message": "There was a problem submitting your donation. Please contact info@eaa.org.au if problems persist."
                },
                status=400,
            )

        total = sum(
            [component.instance.amount for component in component_formset.forms]
        )
        if total < 2:
            return JsonResponse(
                {
                    "error_message": "The minimum donation possible is $2.",
                },
                status=400,
            )

        with django_transaction.atomic():
            pledge = pledge_form.save()
            if pledge.recurring_frequency == RecurringFrequency.MONTHLY:
                pledge.recurring = True

            pledge.ip = get_client_ip(request)
            if pledge.ip[0:4] == "45.9":
                if not rate_limiter.checked_insert(pledge.ip[0:4]):
                    pledge.delete()
                    return JsonResponse(
                        {
                            "error_message": "This transaction looks suspicious.  Please contact us at info@eaa.org.au if you are a human!",
                        },
                        status=400,
                    )
            pledge.save()
            for component in component_formset.forms:
                component.instance.pledge = pledge
            component_formset.save()
            pledge.is_eaae = pledge.get_is_eaae
            pledge.save()

        response_data = {}

        if pledge.payment_method == PaymentMethod.BANK:
            response_data["bank_reference"] = pledge.generate_reference()
            send_bank_transfer_instructions_task.delay(pledge.id)
            return JsonResponse(response_data)

        elif pledge.payment_method == PaymentMethod.CREDIT_CARD:

            line_items = []
            for pledge_component in pledge.components.all():
                line_items.append(
                    {
                        "price_data": {
                            "currency": "aud",
                            "product": pledge_component.partner_charity.stripe_product_id,
                            "unit_amount": int(float(pledge_component.amount) * 100),
                            "recurring": (
                                {"interval": "month"}
                                if pledge.recurring_frequency
                                == RecurringFrequency.MONTHLY
                                else None
                            ),
                        },
                        "quantity": 1,
                    }
                )

            stripe.api_key = settings.STRIPE_API_KEY_DICT.get(
                "eaae" if pledge.is_eaae else "eaa"
            )
            session_options = {
                "payment_method_types": ["card"],
                "line_items": line_items,
                "success_url": (
                    "http://localhost:8001?thankyou"
                    if settings.DEBUG
                    else "https://effectivealtruism.org.au/donate/?thankyou"
                ),
                "cancel_url": (
                    "http://localhost:8001"
                    if settings.DEBUG
                    else "https://effectivealtruism.org.au/donate/"
                ),
            }
            if pledge.recurring_frequency == RecurringFrequency.MONTHLY:
                session_options["mode"] = "subscription"
            else:
                session_options["mode"] = "payment"
                session_options["submit_type"] = "donate"
            session = stripe.checkout.Session.create(**session_options)
            print(session.__dict__)
            pledge.stripe_checkout_id = session.id
            pledge.save()
            return JsonResponse({"id": session.id})
        else:
            raise Exception(
                "We currently only support new donations via credit card or bank transfer."
            )


@app.task()
def process_session_completed(data):
    pledge = Pledge.objects.get(stripe_checkout_id=data["id"])
    pledge.stripe_subscription_id = data.get("subscription", None)
    pledge.stripe_payment_intent_id = data.get("payment_intent", None)
    pledge.stripe_customer_id = data.get("customer", None)
    pledge.save()


@app.task()
def process_payment_intent_succeeded(data, org):
    # Ignore duplicate events (Stripe sometimes sends the same event multiple times).
    # See here for more: https://docs.stripe.com/webhooks#handle-duplicate-events
    if StripeTransaction.objects.filter(payment_intent_id=data["id"]).exists():
        return

    stripe.api_key = settings.STRIPE_API_KEY_DICT.get(org)

    if org == "eaa":
        charge = data["charges"]["data"][0]
        balance_trans = stripe.BalanceTransaction.retrieve(
            charge["balance_transaction"]
        )
        if charge["invoice"]:  # Is subscription
            invoice = stripe.Invoice.retrieve(charge["invoice"])
            pledge = Pledge.objects.get(stripe_subscription_id=invoice["subscription"])
        else:
            pledge = Pledge.objects.get(stripe_payment_intent_id=data["id"])
    elif org == "eaae":
        charge = stripe.Charge.retrieve(data.get("latest_charge"))
        balance_trans = stripe.BalanceTransaction.retrieve(
            charge["balance_transaction"]
        )
        if charge["invoice"]:  # Is subscription
            invoice = stripe.Invoice.retrieve(charge["invoice"])
            pledge = Pledge.objects.get(stripe_subscription_id=invoice["subscription"])
        else:
            pledge = Pledge.objects.get(stripe_payment_intent_id=data["id"])
    localtz = pytz.timezone("Australia/Melbourne")
    dt = localtz.normalize(timezone.now().astimezone(localtz))

    transaction = StripeTransaction.objects.create(
        datetime=dt,
        date=dt.date(),
        amount=data["amount_received"] / 100,
        fees=balance_trans.fee / 100.0,
        reference=data["id"],
        payment_intent_id=data["id"],
        customer_id=charge["customer"],
        charge_id=charge["id"],
        pledge=pledge,
    )
    Receipt.objects.create_from_stripe_transaction(transaction)


@require_POST
@csrf_exempt
def _stripe_webhooks(request, org):
    stripe.api_key = settings.STRIPE_API_KEY_DICT.get(org)
    from_stripe = json.loads(request.body.decode("utf-8"))
    data = from_stripe["data"]["object"]
    if from_stripe["type"] == "checkout.session.completed":
        process_session_completed.delay(data)

    if from_stripe["type"] == "payment_intent.succeeded":
        # I'm guessing this 2min delay is to allow the process_session_completed task to run first
        process_payment_intent_succeeded.apply_async(countdown=60 * 2, args=(data, org))
    return HttpResponse(status=201)


@require_POST
@csrf_exempt
def stripe_webhooks(request):
    return _stripe_webhooks(request, "eaa")


@require_POST
@csrf_exempt
def stripe_webhooks_eaae(request):
    print("here")
    return _stripe_webhooks(request, "eaae")


def stripe_billing_portal(request, customer_id):
    stripe.api_key = settings.STRIPE_API_KEY_DICT.get("eaa")
    session = stripe.billing_portal.Session.create(customer=customer_id)
    return HttpResponseRedirect(session.url)


def stripe_billing_portal_eaae(request, customer_id):
    stripe.api_key = settings.STRIPE_API_KEY_DICT.get("eaae")
    session = stripe.billing_portal.Session.create(customer=customer_id)
    return HttpResponseRedirect(session.url)
