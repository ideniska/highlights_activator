from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .kindle_parser import start_kindle_parser
from .forms import FileForm
from django.core.files.storage import FileSystemStorage
from .models import UserFiles, Quote
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


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


class ByBookView(LoginRequiredMixin, TemplateView):
    template_name = "by_book.html"


class ByTagView(LoginRequiredMixin, TemplateView):
    template_name = "by_tag.html"


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
            user_file_name_obj = UserFiles.objects.filter(
                owner=form.instance.owner
            ).latest("uploaded_at")
            field_name = "file"
            user_file_name_value = getattr(user_file_name_obj, field_name)
            start_kindle_parser(
                "media/" + str(user_file_name_value), form.instance.owner.id
            )
            return redirect("dashboard")
    else:
        form = FileForm()
    return render(request, "upload.html", {"form": form})
