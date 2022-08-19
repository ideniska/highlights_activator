from django.urls import path
from .views import (
    api_home,
    BookListAPIView,
    BookDetailAPIView,
    BookVisibilityView,
    RandomQuoteAPIView,
    QuoteLikeView,
)

urlpatterns = [
    path("by-book/", BookListAPIView.as_view()),
    path("<int:pk>/", BookDetailAPIView.as_view()),
    path("book/<int:pk>/visibility/", BookVisibilityView.as_view()),
    path("quote/<int:pk>/like/", QuoteLikeView.as_view()),
    path("random/", RandomQuoteAPIView.as_view()),
]
