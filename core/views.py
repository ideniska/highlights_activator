from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .kindle_parser import start_kindle_parser
from .forms import FileForm
from django.core.files.storage import FileSystemStorage


class HomePageView(TemplateView):
    template_name = 'home.html'


class LandingPageView(TemplateView):
    template_name = 'landing.html'


class DashboardPageView(TemplateView):
    template_name = 'dashboard.html'


# FILE UPLOAD
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.owner = request.user #gets the file file owner from current user
            form.save()
            return redirect('dashboard')
    else:
        form = FileForm()
    return render(request, 'upload.html', {
        'form': form
    }) 