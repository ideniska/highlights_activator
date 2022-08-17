from django.urls import path
from .views import api_home, BookListAPIView, BookDetailAPIView, BookVisibilityView

urlpatterns = [
    path("by-book/", BookListAPIView.as_view()),
    path("<int:pk>/", BookDetailAPIView.as_view()),
    path("book/<int:pk>/visibility/", BookVisibilityView.as_view()),
]