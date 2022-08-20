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
    TemplateAPIView,
    BooksTemplateAPIView,
)

urlpatterns = [
    path("dashboard/", DashboardPageView.as_view(), name="dashboard"),
    path(
        "dashboard-api/",
        TemplateAPIView.as_view(template_name="dashboard_api.html"),
        name="dashboard-api",
    ),
    path(
        "favorite/",
        TemplateAPIView.as_view(template_name="favorite.html"),
        name="favorite",
    ),
    path(
        "daily/",
        TemplateAPIView.as_view(template_name="daily.html"),
        name="daily",
    ),
    path("", LandingPageView.as_view(), name="landing"),
    path("upload/", upload_file, name="upload"),
    path("smart_feed/", SmartFeedView.as_view(), name="smart_feed"),
    path("by_book/", ByBookView.as_view(), name="by_book"),
    path(
        "by-book-api/",
        BooksTemplateAPIView.as_view(template_name="by_book_api.html"),
        name="by-book-api",
    ),
    path("by-book/<int:id>", book_inside_view, name="book_page"),
    path("by-book-api/<int:id>", book_inside_view, name="book_page"),
    path("by-tag/", ByTagView.as_view(), name="by_tag"),
    path("logout/", logout_user, name="logout"),
]
