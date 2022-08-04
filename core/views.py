from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'

class LandingPageView(TemplateView):
    template_name = 'landing.html'
