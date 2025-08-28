# Note: the pinpayments app (which is installed) already supplies "pin_payment_tags" so this file must
# be named differently.

from django import template

from pinpayments.templatetags.pin_payment_tags import pin_header, pin_form

register = template.Library()

register.inclusion_tag("pinpayments/modified_pin_headers.html", takes_context=True)(
    pin_header
)
register.inclusion_tag("pinpayments/modified_pin_form.html", takes_context=True)(
    pin_form
)
