from django.urls import path
from .views import (
    HomePageView,
    LandingPageView,
    DashboardPageView,
    SmartFeedView,
    ByBookView,
    ByTagView,
    logout_user,
    book_inside_view,
    upload_file,
)

urlpatterns = [
    path("dashboard/", DashboardPageView.as_view(), name="dashboard"),
    path("", LandingPageView.as_view(), name="landing"),
    path("upload/", upload_file, name="upload"),
    path("smart_feed/", SmartFeedView.as_view(), name="smart_feed"),
    path("by_book/", ByBookView.as_view(), name="by_book"),
    path("by_book/<int:id>", book_inside_view, name="book_page"),
    path("by_tag/", ByTagView.as_view(), name="by_tag"),
    path("logout/", logout_user, name="logout"),
]
