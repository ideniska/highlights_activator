from gc import get_objects
from multiprocessing import context
from urllib import request
from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .kindle_parser import start_kindle_parser
from .forms import FileForm
from django.core.files.storage import FileSystemStorage
from .models import UserFile, Quote, Book
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
from .pagination import PageNumberPagination
from django.core.mail import send_mail
from core.tasks import celery_get_book_covers
from .permissions import PaidUser
from django.views import View
import stripe
from django.conf import settings


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


class HomePageView(TemplateAPIView):
    template_name = "home.html"


class SettingsPageView(TemplateAPIView):
    # permission_classes = (PaidUser,)
    template_name = "settings.html"


class LoginPageView(TemplateAPIView):
    permission_classes = (AllowAny,)
    template_name = "login.html"


class RegisterPageView(TemplateAPIView):
    permission_classes = (AllowAny,)
    template_name = "register.html"


class LandingPageView(TemplateAPIView):
    permission_classes = (AllowAny,)
    template_name = "landing.html"


class DashboardPageView(LoginRequiredMixin, ListView):
    template_name = "dashboard.html"
    model = Quote
    context_object_name = "random_quote"

    # Get all quotes whos owner is current user, pick random,
    # return when context_object_name is called in a template
    def get_queryset(self):
        items = list(Quote.objects.filter(owner=self.request.user.id))
        if items:
            return random.choice(items)


class SmartFeedView(LoginRequiredMixin, TemplateView):
    template_name = "smart_feed.html"


# class ByBookView(LoginRequiredMixin, ListView):
#     template_name = "by_book.html"
#     model = Quote
#     context_object_name = "highlights_count"

#     def get_queryset(self):
#         quotes_list = list(Quote.objects.filter(owner=self.request.user.id))

#         # Count how many highlights in each book
#         highlights = {}
#         for record in quotes_list:
#             book_title = record.book_title_db
#             quote = record.quote_db
#             if book_title not in highlights:
#                 highlights[book_title] = [quote]
#             else:
#                 highlights[book_title].append(quote)

#         highlights_count = {}
#         for key in highlights:
#             highlights_count[key] = len(highlights[key])

#         # Return dict with books as keys and highlights count as values
#         return highlights_count.items()


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


# # FILE UPLOAD
# def upload_file(request):
#     if request.method == "POST":
#         form = FileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.instance.owner = (
#                 request.user
#             )  # gets the file file owner from current user
#             form.save()
#             user_file_name_obj = UserFile.objects.latest("uploaded_at")
#             field_name = "file"
#             user_file_path = getattr(user_file_name_obj, field_name)
#             start_kindle_parser(str(user_file_path), request.user)
#             # celery_get_book_covers(request.user.id)
#             return redirect("dashboard")
#     else:
#         form = FileForm()
#     return render(request, "upload.html", {"form": form})


class UploadView(TemplateAPIView):
    template_name = "upload.html"


# def logout_user(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("landing"))


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
# stripe.api_key = "sk_test_51HUbRSL00h3ctAIbxVXwW3QyCIgz7tuvndipLv5IiX702yy5OEqbeHYLxPU98fJPPm1FNWvMT3IgQVGFSvrcvLlO00wFkqcISb"
YOUR_DOMAIN = "http://127.0.0.1:8000/"
# TODO move to settings.py


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
        # return JsonResponse(
        #     {
        #         "id": checkout_session.id,
        #     }
        # )


class CreatePortalSessionView(View):
    def post(self, request, *args, **kwargs):
        # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
        # Typically this is stored alongside the authenticated user in your database.
        checkout_session_id = request.form.get("session_id")
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

        # This is the URL to which the customer will be redirected after they are
        # done managing their billing with the portal.
        return_url = YOUR_DOMAIN + "/dashboard"

        portalSession = stripe.billing_portal.Session.create(
            customer=checkout_session.customer,
            return_url=return_url,
        )
        return HttpResponseRedirect(portalSession.url)
