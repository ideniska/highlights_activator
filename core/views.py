from django.views.generic import TemplateView
from django.views.generic.list import ListView


class HomePageView(TemplateView):
    template_name = 'home.html'


class LandingPageView(TemplateView):
    template_name = 'landing.html'


class DashboardPageView(TemplateView):
    template_name = 'dashboard.html'