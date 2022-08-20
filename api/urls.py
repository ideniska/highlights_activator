from django.urls import path
from .views import (
    api_home,
    BookListAPIView,
    BookVisibilityView,
    QuoteLikeView,
    FavoriteQuotesAPIView,
    RandomServerQuoteAPIView,
    QuotesFromBookAPIView,
)

urlpatterns = [
    path("by-book/", BookListAPIView.as_view()),
    path("by-book/<int:pk>/", QuotesFromBookAPIView.as_view()),
    path("book/<int:pk>/visibility/", BookVisibilityView.as_view()),
    path("quote/<int:pk>/like/", QuoteLikeView.as_view()),
    path("random/", RandomServerQuoteAPIView.as_view()),
    path("favorites/", FavoriteQuotesAPIView.as_view()),
]
