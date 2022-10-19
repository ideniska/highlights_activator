from gc import get_objects
from multiprocessing import context
from os import PRIO_USER
from urllib import request
from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .kindle_parser import start_kindle_parser
from .forms import FileForm
from django.core.files.storage import FileSystemStorage
from .models import Orders, UserFile, Quote, Book
from api.serializers import BookSerializer
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .pagination import PageNumberPagination
from django.core.mail import send_mail
from core.tasks import celery_get_book_covers
from core.notifications import EmailService
from .permissions import PaidUser
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from typing import TypeVar
from django.utils import timezone
import datetime
from project.settings import YOUR_DOMAIN

UserType = TypeVar("UserType", bound="CustomUser")
User = get_user_model()


class TemplateAPIView(APIView):
    """Help to build CMS System using DRF, JWT and Cookies
    path('some-path/', TemplateAPIView.as_view(template_name='template.html'))
    """

    # # login_url = "/login/"
    # # redirect_field_name = "login"
    swagger_schema = None
    # permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)
    template_name: str = ""

    def get(self, request, *args, **kwargs):
        return Response()


class AuthenticatedTemplateAPIView(TemplateAPIView):
    def dispatch(self, *args, **kwargs):
        a = super().dispatch(*args, **kwargs)
        if not self.request.user.is_authenticated:
            return redirect("landing")
        return a


class HomePageView(TemplateAPIView):
    template_name: str = "home.html"


class DashboardPageView(AuthenticatedTemplateAPIView):
    template_name: str = "dashboard_api.html"


class SettingsPageView(AuthenticatedTemplateAPIView):
    # permission_classes = (PaidUser,)
    template_name: str = "settings.html"


class LoginPageView(TemplateAPIView):
    permission_classes = (AllowAny,)
    template_name: str = "login.html"


class ActivationPageView(TemplateAPIView):
    permission_classes = (AllowAny,)
    template_name: str = "confirm_email.html"


class SetNewPassPageView(TemplateAPIView):
    permission_classes = (AllowAny,)
    template_name: str = "set_password.html"


class ForgotPasswordPageView(TemplateAPIView):
    permission_classes = (AllowAny,)
    template_name: str = "forgot_password.html"


class CheckEmailPasswordPageView(TemplateAPIView):
    permission_classes = (AllowAny,)
    template_name: str = "check_email_for_password.html"


class EmailActivatePageView(TemplateAPIView):
    permission_classes = (AllowAny,)
    template_name: str = "email_activate.html"


class RegisterPageView(TemplateAPIView):
    permission_classes = (AllowAny,)
    template_name: str = "register.html"


class LandingPageView(TemplateAPIView):
    permission_classes = (AllowAny,)
    template_name: str = "landing.html"


class SmartFeedView(ActivationPageView):
    template_name: str = "smart_feed.html"


class ByBookView(LoginRequiredMixin, ListView):
    template_name = "by_book.html"
    # model = Book
    context_object_name = "books"

    def get_queryset(self):
        return Book.objects.filter(owner=self.request.user).annotate(
            quotes_count=Count("quotes")
        )  # annotate creates a variable quotes_count for each book object and uses Count method to count related quotes


class ByTagView(LoginRequiredMixin, TemplateView):
    template_name = "by_tag.html"


def book_inside_view(request, id):
    list_of_quotes = get_list_or_404(Quote, book=id)
    book_title = get_object_or_404(Book, id=id)
    context = {"quotes_by_book": list_of_quotes, "book_title": book_title.title}
    return render(request, "book_page.html", context)


class UploadView(ActivationPageView):
    template_name: str = "upload.html"


class BooksTemplateAPIView(APIView):
    """Help to build CMS System using DRF, JWT and Cookies
    path('some-path/', TemplateAPIView.as_view(template_name='template.html'))
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    swagger_schema = None
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)
    template_name: str = ""
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response()

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = settings.YOUR_DOMAIN


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
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


class CreatePortalSessionView(APIView):
    def post(self, request, *args, **kwargs):
        # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
        # Typically this is stored alongside the authenticated user in your database.
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


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # if event["type"] == "invoice.paid":
    #     stripe_invoice_id = event["data"]["object"]["id"]

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        stripe_user_email = session["customer_details"]["email"]
        stripe_payment_status = session["payment_status"]
        stripe_payment_data = stripe.checkout.Session.list_line_items(
            session["id"], limit=1
        )
        product = stripe_payment_data["data"][0]["description"]
        price_paid = stripe_payment_data["data"][0]["amount_total"] / 100

        if stripe_payment_status == "paid":
            user = User.objects.get(email=stripe_user_email)
            user.active_subscription = True

            if "1 month" in product:
                subscription_period = 30
            else:
                subscription_period = 365
            if user.paid_until == None:
                user.paid_until = timezone.now() + datetime.timedelta(
                    days=subscription_period
                )
            else:
                user.paid_until += datetime.timedelta(days=subscription_period)
            user.stripe_session_id = session["id"]
            user.save()

            order = Orders.objects.create(
                user=user,
                stripe_user_email=stripe_user_email,
                order_type="Subscription",
                price=price_paid,
                payment_status="active",
                subscription_period=subscription_period,
                payment_date=timezone.now(),
            )
            order.save()
            email = EmailService()
            email.send_payment_confirmation(user, YOUR_DOMAIN)
            print(request.user)
    return HttpResponse(status=200)
