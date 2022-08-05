from django.urls import path

from .views import HomePageView, LandingPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('landing/', LandingPageView.as_view(), name='landing'),
]

