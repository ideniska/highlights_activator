from django.urls import path

from .views import HomePageView, LandingPageView, DashboardPageView

urlpatterns = [
    path('dashboard', DashboardPageView.as_view(), name='dashboard'),
    path('', LandingPageView.as_view(), name='landing'),
]

