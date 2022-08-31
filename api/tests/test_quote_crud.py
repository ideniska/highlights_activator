from http.client import responses
from turtle import title
import pytest
from django.urls import reverse

from core.models import Book, Quote

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def book(user) -> Book:
    return Book.objects.create(title="Test book", owner=user)


@pytest.fixture
def quote(user, book) -> Quote:
    return Quote.objects.create(
        book=book,
        date_added="Added on Sunday, March 24, 2019 7:50:17 AM",
        text="Test quote",
        owner=user,
        comment="",
    )


def test_quote_delete(user, quote, client):
    url = reverse("quote_delete", kwargs={"pk": quote.id})
    response = client.delete(url)
    assert response.status_code == 204, response.data


def test_quote_delete_no_quote(user, client):
    url = reverse("quote_delete", kwargs={"pk": 2})
    response = client.delete(url)
    assert response.status_code == 204, response.data
