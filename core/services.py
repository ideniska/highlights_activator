import stripe
from django.conf import settings
from typing import TypeVar
from django.utils import timezone
import datetime
from project.settings import YOUR_DOMAIN
from django.http import HttpResponseRedirect


stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = settings.YOUR_DOMAIN


class CreateCheckoutSessionService:
    def create_checkout_session(self, request):
        prices = stripe.Price.list(
            lookup_keys=[request.POST["lookup_key"]], expand=["data.product"]
        )
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": prices.data[0].id,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=YOUR_DOMAIN + "stripe/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=YOUR_DOMAIN + "stripe/cancel",
        )
        return HttpResponseRedirect(checkout_session.url)


class CreatePortalSessionService:
    def create_portal_session(self, request):
        checkout_session_id = request.user.stripe_session_id
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

        # This is the URL to which the customer will be redirected after they are
        # done managing their billing with the portal.
        return_url = YOUR_DOMAIN + "dashboard"

        portalSession = stripe.billing_portal.Session.create(
            customer=checkout_session.customer,
            return_url=return_url,
        )
        return HttpResponseRedirect(portalSession.url)
