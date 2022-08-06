from django.urls import path
from .views import upload_file

from .views import (
    HomePageView,
    LandingPageView,
    DashboardPageView,
    SmartFeedView,
    ByBookView,
    ByTagView,
)

urlpatterns = [
    path("dashboard/", DashboardPageView.as_view(), name="dashboard"),
    path("", LandingPageView.as_view(), name="landing"),
    path("upload/", upload_file, name="upload"),
    path("smart_feed/", SmartFeedView.as_view(), name="smart_feed"),
    path("by_book/", ByBookView.as_view(), name="by_book"),
    path("by_tag/", ByTagView.as_view(), name="by_tag"),
]
