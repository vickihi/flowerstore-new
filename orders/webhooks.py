import os
import logging
import json
import stripe

from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import Order

logger = logging.getLogger(__name__)


def _format_address_one_line(address) -> str:
    """Convert an address payload/string into a single-line display value."""
    if not address:
        return "N/A"

    data = address
    if isinstance(address, str):
        try:
            data = json.loads(address)
        except (TypeError, json.JSONDecodeError):
            return address.replace("\n", ", ").strip()

    if isinstance(data, dict):
        parts = [
            data.get("line1"),
            data.get("line2"),
            data.get("city"),
            data.get("state"),
            data.get("postal_code"),
            data.get("country"),
        ]
        return ", ".join(str(part).strip() for part in parts if part)

    return str(data).replace("\n", ", ").strip()


def _send_order_confirmation_email(order: Order) -> None:
    """Send an order confirmation email after payment is fulfilled."""
    if not order.customer_email:
        return

    item_lines = [
        f"- {item.product.name} x {item.quantity} @ ${item.unit_price}"
        for item in order.items.select_related("product").all()
    ]
    items_text = "\n".join(item_lines) if item_lines else "- No items found"

    subject = f"Order Confirmation #{order.id}"
    message = (
        f"Hi {order.customer_name or 'Customer'},\n\n"
        "Thank you for your purchase from our flower shop.\n"
        f"We have received your order #{order.id}.\n\n"
        "Order summary:\n"
        f"{items_text}\n\n"
        f"Total paid: ${order.total_price}\n\n"
        "Shipping address: "
        f"{_format_address_one_line(order.ship_address or order.bill_address)}\n\n"
        "If you have any questions, please reply to this email: info@flowerstore.ca .\n"
    )

    from_email = "no-reply@flowerstore.ca"
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[order.customer_email],
        fail_silently=False,
    )


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe events."""
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    if not sig_header:
        return HttpResponse(status=400)

    event = None
    endpoint_secret = os.environ["STRIPE_WEBHOOK_SECRET"]

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as _:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as _:
        return HttpResponse(status=400)

    is_checkout_event = (
        event["type"] == "checkout.session.completed"
        or event["type"] == "checkout.session.async_payment_succeeded"
    )

    if is_checkout_event:
        session = event["data"]["object"]
        session_dict = session if isinstance(session, dict) else session.to_dict()

        if session_dict.get("payment_status") != "paid":
            return HttpResponse(status=200)

        order_id = session_dict.get("client_reference_id")
        if not order_id:
            return HttpResponse(status=400)
        try:
            order = Order.objects.get(pk=order_id)
        except (Order.DoesNotExist, ValueError, TypeError, ValidationError):
            return HttpResponse(status=400)

        if order.is_fulfilled:
            return HttpResponse(status=200)

        customer_details = session_dict.get("customer_details") or {}
        shipping_details = (
            session_dict.get("shipping_details")
            or (session_dict.get("collected_information") or {}).get("shipping_details")
            or {}
        )
        account_name = (
            order.user.full_name.strip()
            if order.user and getattr(order.user, "full_name", "")
            else ""
        )

        order.fulfill(
            name=(
                account_name
                or customer_details.get("name")
                or shipping_details.get("name")
                or ""
            ),
            email=customer_details.get("email", ""),
            payment_id=session_dict.get("payment_intent"),
            billing_address=customer_details.get("address"),
            shipping_address=shipping_details.get("address"),
        )
        try:
            _send_order_confirmation_email(order)
        except Exception:
            logger.exception(
                "Failed to send order confirmation email for order_id=%s", order.id
            )

    return HttpResponse(status=200)
