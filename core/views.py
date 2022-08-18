from gc import get_objects
from multiprocessing import context
from urllib import request
from django.views.generic import TemplateView, DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .kindle_parser import start_kindle_parser
from .forms import FileForm
from django.core.files.storage import FileSystemStorage
from .models import UserFile, Quote, Book
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


User = get_user_model()


class HomePageView(TemplateView):
    template_name = "home.html"


class LandingPageView(TemplateView):
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


@login_required
def book_inside_view(request, id):
    list_of_quotes = get_list_or_404(Quote, book_title_db=id)
    book_title = get_object_or_404(Book, id=id)
    context = {"quotes_by_book": list_of_quotes, "book_title": book_title.book_title_db}
    return render(request, "book_page.html", context)


# FILE UPLOAD
@login_required
def upload_file(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = (
                request.user
            )  # gets the file file owner from current user
            form.save()
            user_file_name_obj = UserFile.objects.latest("uploaded_at")
            field_name = "file"
            user_file_path = getattr(user_file_name_obj, field_name)
            start_kindle_parser("media/" + str(user_file_path), request.user)
            return redirect("dashboard")
    else:
        form = FileForm()
    return render(request, "upload.html", {"form": form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("landing"))


class TemplateAPIView(APIView):
    """Help to build CMS System using DRF, JWT and Cookies
    path('some-path/', TemplateAPIView.as_view(template_name='template.html'))
    """

    swagger_schema = None
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)
    template_name: str = ""

    def get(self, request, *args, **kwargs):
        return Response()
