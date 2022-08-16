from django.urls import path
from .views import api_home, BookListAPIView, BookDetailAPIView

urlpatterns = [
    path("", BookListAPIView.as_view()),
    path("<int:pk>/", BookDetailAPIView.as_view()),
]
