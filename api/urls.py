from django.urls import path
from .views import (
    api_home,
    BookListAPIView,
    BookDetailAPIView,
    BookVisibilityView,
    QuoteLikeView,
    FavoriteQuotesAPIView,
    RandomServerQuoteAPIView,
)

urlpatterns = [
    path("by-book/", BookListAPIView.as_view()),
    path("<int:pk>/", BookDetailAPIView.as_view()),
    path("book/<int:pk>/visibility/", BookVisibilityView.as_view()),
    path("quote/<int:pk>/like/", QuoteLikeView.as_view()),
    path("random/", RandomServerQuoteAPIView.as_view()),
    path("favorites/", FavoriteQuotesAPIView.as_view()),
]
