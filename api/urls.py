from django.urls import path
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
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path("auth/", obtain_auth_token),
    path("by-book/", BookListAPIView.as_view()),
    path("by-book/<int:pk>/", QuotesFromBookAPIView.as_view(), name="book_page"),
    path("book/<int:pk>/visibility/", BookVisibilityView.as_view()),
    path("quote/<int:pk>/like/", QuoteLikeView.as_view()),
    path("quote/<int:pk>/delete/", QuoteDeleteView.as_view()),
    path("random/", RandomServerQuoteAPIView.as_view()),
    path("favorites/", FavoriteQuotesAPIView.as_view()),
    path("daily/", DailyTenAPIView.as_view()),
]
