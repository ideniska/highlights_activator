import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions, authentication
from core.models import Book, Quote
from .serializers import BookSerializer, QuoteSerializer
from core.pagination import BasePageNumberPagination
from django.db.models import Count
import random


@api_view(["POST"])
def api_home(request, *args, **kwargs):
    return Response(request.data)


class BookListAPIView(
    generics.ListCreateAPIView,
):

    queryset = Book.objects.annotate(quotes_count=Count("quotes"))
    serializer_class = BookSerializer
    pagination_class = BasePageNumberPagination

    # def get_queryset(self):
    #     return Book.objects.filter(owner=self.request.user).annotate(
    #         quotes_count=Count("quotes")
    #     )  # annotate creates a variable quotes_count for each book object and uses Count method to count related quotes

    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    # def perform_create(self, serializer):
    #     # serializer.save(user=self.request.user)
    #     title = serializer.validated_data.get("title")
    #     content = serializer.validated_data.get("content") or None
    #     if content is None:
    #         content = title
    #     serializer.save(content=content)


class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class RandomQuoteAPIView(
    generics.ListCreateAPIView,
):

    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


# class BookVisibilityView(generics.GenericAPIView):
#     def post(self, request, pk: int):
#         try:
#             book = Book.objects.get(id=pk)
#             print(book)
#         except Book.DoesNotExist:
#             return Response({"detail": "not found"}, status=404)

#         return Response({})
