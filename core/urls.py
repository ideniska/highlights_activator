from django.urls import path
from .views import upload_file

from .views import HomePageView, LandingPageView, DashboardPageView

urlpatterns = [
    path('dashboard', DashboardPageView.as_view(), name='dashboard'),
    path('', LandingPageView.as_view(), name='landing'),
    path('upload', upload_file, name='upload'),
]

