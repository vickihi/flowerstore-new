import os
import stripe

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Order


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe events."""
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    endpoint_secret = os.environ["STRIPE_WEBHOOK_SECRET"]

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as _:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as _:
        return HttpResponse(status=400)

    is_payment_fulfilled = (
        event["type"] == "checkout.session.completed"
        or event["type"] == "checkout.session.async_payment_succeeded"
    )

    if is_payment_fulfilled:
        stripe_checkout_session = event["data"]["object"]
        order_id = stripe_checkout_session["client_reference_id"]
        order = Order.objects.get(pk=order_id)

        customer_details = stripe_checkout_session.get("customer_details") or {}
        shipping_details = (
            stripe_checkout_session.get("shipping_details") 
            or stripe_checkout_session.get("collected_information", {}).get("shipping_details")
            or {}
        )

        order.fulfill(
            name=(
                shipping_details.get("name")
                or customer_details.get("name")
                or ""
            ),
            email=customer_details.get("email", ""),
            payment_id=stripe_checkout_session["payment_intent"], 
            billing_address=customer_details.get("address"),
            shipping_address=shipping_details.get("address"),
        )

    return HttpResponse(status=200)
