from django.urls import path, include
from .views import (
    api_home,
    BookListAPIView,
    BookVisibilityView,
    QuoteLikeView,
    FavoriteQuotesAPIView,
    RandomServerQuoteAPIView,
    QuotesFromBookAPIView,
    DailyTenAPIView,
    QuoteDeleteView,
    QuoteUpdateView,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path("auth/", obtain_auth_token),
    path("by-book/", BookListAPIView.as_view(), name="by_book"),
    path("by-book/<int:pk>/", QuotesFromBookAPIView.as_view(), name="book_page"),
    path(
        "book/<int:pk>/visibility/",
        BookVisibilityView.as_view(),
        name="book_visibility",
    ),
    path("quote/<int:pk>/like/", QuoteLikeView.as_view(), name="quote_like"),
    path("quote/<int:pk>/delete/", QuoteDeleteView.as_view(), name="quote_delete"),
    path("quote/<int:pk>/update/", QuoteUpdateView.as_view(), name="quote_update"),
    path("random/", RandomServerQuoteAPIView.as_view(), name="random_quote"),
    path("favorites/", FavoriteQuotesAPIView.as_view(), name="favorite_quote"),
    path("daily/", DailyTenAPIView.as_view(), name="daily_quotes"),
    path("", include("api.auth.urls")),
]
