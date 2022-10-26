from django.urls import path
from . import views

urlpatterns = [
    path(
        "connect/",
        views.ConnectTelegramBotView.as_view(),
        name="connect_telegram",
    ),
    path(
        "random-quote/",
        views.TelegramRandomServerQuoteAPIView.as_view(),
        name="random_telegram_quote",
    ),
]
