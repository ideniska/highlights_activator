from re import template
from django.urls import path
from . import views

urlpatterns = [
    path(
        "daily/",
        views.TemplateAPIView.as_view(template_name="daily.html"),
        name="daily-api",
    ),
    path(
        "dashboard/",
        views.TemplateAPIView.as_view(template_name="dashboard_api.html"),
        name="dashboard",
    ),
    path(
        "favorite/",
        views.TemplateAPIView.as_view(template_name="favorite.html"),
        name="favorite",
    ),
    path(
        "daily/",
        views.TemplateAPIView.as_view(template_name="daily.html"),
        name="daily",
    ),
    path("", views.LandingPageView.as_view(), name="landing"),
    path(
        "upload/",
        views.TemplateAPIView.as_view(template_name="upload.html"),
        name="upload",
    ),
    path(
        "upload-progress/",
        views.TemplateAPIView.as_view(template_name="upload_wait.html"),
        name="upload-progress",
    ),
    path("smart_feed/", views.SmartFeedView.as_view(), name="smart_feed"),
    path("by_book/", views.ByBookView.as_view(), name="by_book"),
    path(
        "by-book-api/",
        views.BooksTemplateAPIView.as_view(template_name="by_book_api.html"),
        name="by-book-api",
    ),
    path("by-book/<int:id>", views.book_inside_view, name="book_page"),
    path(
        "by-book-api/<int:id>",
        views.TemplateAPIView.as_view(template_name="book_page.html"),
    ),
    path("by-tag/", views.ByTagView.as_view(), name="by_tag"),
    path(
        "logout/",
        views.TemplateAPIView.as_view(template_name="logout.html"),
        name="logout_page",
    ),
    path(
        "login/",
        views.LoginPageView.as_view(),
        name="login_page",
    ),
    path(
        "activate/<uid>/<token>/",
        views.TemplateAPIView.as_view(template_name="email_activate.html"),
        name="email_activate",
    ),
    path(
        "register/",
        views.RegisterPageView.as_view(),
        name="register_page",
    ),
    path(
        "activation/",
        views.TemplateAPIView.as_view(template_name="confirm_email.html"),
        name="activation",
    ),
    path(
        "settings/",
        views.SettingsPageView.as_view(),
        name="settings",
    ),
    path(
        "create-checkout-session/",
        views.CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path(
        "checkout/",
        views.TemplateAPIView.as_view(template_name="stripe/checkout.html"),
        name="checkout",
    ),
    path(
        "stripe/success/",
        views.TemplateAPIView.as_view(template_name="stripe/success.html"),
        name="success",
    ),
    path(
        "stripe/cancel/",
        views.TemplateAPIView.as_view(template_name="stripe/dashboard_api.html"),
        name="cancel",
    ),
]
