from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.SignInView.as_view(), name="api_login"),
    path("logout/", views.SignOutView.as_view(), name="api_logout"),
    path("register/", views.SignUpView.as_view(), name="api_register"),
    path(
        "activate/",
        views.ActivateView.as_view(),
        name="activate",
    ),
]
