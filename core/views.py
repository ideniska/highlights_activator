from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .kindle_parser import start_kindle_parser
from .forms import FileForm
from django.core.files.storage import FileSystemStorage
from .models import UserFiles, Quote


# from kindle_parser import start_kindle_parser


class HomePageView(TemplateView):
    template_name = "home.html"


class LandingPageView(TemplateView):
    template_name = "landing.html"


class DashboardPageView(TemplateView):
    template_name = "dashboard.html"
    # model = Quote
    # context_object_name = Quote.objects.filter(owner=user=self.request.user)


class SmartFeedView(TemplateView):
    template_name = "smart_feed.html"


class ByBookView(TemplateView):
    template_name = "by_book.html"


class ByTagView(TemplateView):
    template_name = "by_tag.html"


# FILE UPLOAD
def upload_file(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = (
                request.user
            )  # gets the file file owner from current user
            form.save()
            # user_file_name_obj = UserFiles.objects.all().filter(owner=form.instance.owner )
            user_file_name_obj = UserFiles.objects.filter(
                owner=form.instance.owner
            ).latest("uploaded_at")
            field_name = "file"
            user_file_name_value = getattr(user_file_name_obj, field_name)
            # print('user_file_name is:', user_file_name_value)
            # print('owner is: ', form.instance.owner)
            start_kindle_parser(
                "media/" + str(user_file_name_value), form.instance.owner.id
            )
            return redirect("dashboard")
    else:
        form = FileForm()
    return render(request, "upload.html", {"form": form})
