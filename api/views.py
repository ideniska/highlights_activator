import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions, authentication
from core.models import Book, Quote
from .serializers import BookSerializer


@api_view(["POST"])
def api_home(request, *args, **kwargs):
    return Response(request.data)


class BookListAPIView(
    generics.ListCreateAPIView,
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
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
