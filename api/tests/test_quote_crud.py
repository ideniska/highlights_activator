from traceback import print_tb
import pytest
from django.urls import reverse


from core.models import Book, Quote

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def book(user) -> Book:
    return Book.objects.create(title="Test book", owner=user)


@pytest.fixture
def books(user) -> list[Book]:
    return Book.objects.bulk_create(
        [
            Book(title="Test book", owner=user),
            Book(title="Test book2", owner=user),
            Book(title="Test book3", owner=user),
            Book(title="Test book4", owner=user),
        ]
    )


@pytest.fixture
def quote(user, book) -> Quote:
    return Quote.objects.create(
        book=book,
        date_added="Added on Sunday, March 24, 2019 7:50:17 AM",
        text="Test quote",
        owner=user,
        comment="",
    )


@pytest.fixture
def quotes(user, book):
    return Quote.objects.bulk_create(
        [
            Quote(
                book=book,
                date_added="Added on Sunday, March 24, 2019 7:50:17 AM",
                text="Test quote1",
                owner=user,
                comment="",
            ),
            Quote(
                book=book,
                date_added="Added on Sunday, March 24, 2019 7:50:17 AM",
                text="Test quote2",
                owner=user,
                comment="",
            ),
            Quote(
                book=book,
                date_added="Added on Sunday, March 24, 2019 7:50:17 AM",
                text="Test quote3",
                owner=user,
                comment="",
            ),
            Quote(
                book=book,
                date_added="Added on Sunday, March 24, 2019 7:50:17 AM",
                text="Test quote4",
                owner=user,
                comment="",
            ),
        ]
    )


# DELETE A QUOTE
def test_quote_delete_with_auth(user, quote, api_client):
    """Authorized user deletes a quote"""

    url = reverse("quote_delete", kwargs={"pk": quote.id})
    response = api_client.delete(url)

    assert response.status_code == 204, response.data
    assert not Quote.objects.filter(id=quote.id).exists()
    # TODO CAN ONE USER DELETE QUOTE OF OTHER USER


def test_quote_delete_no_auth(quote, client):
    """Unauthorized user deletes a quote"""

    url = reverse("quote_delete", kwargs={"pk": quote.id})
    response = client.delete(url)
    assert response.status_code == 403, response.data
    # TODO WHY SERVER RESPONDS FORBIDDEN 403 and not 401 which is Unauthorized?


def test_quote_delete_no_quote(user, client):
    """Authorized user deletes a quote which doesn't exist in DB"""

    url = reverse("quote_delete", kwargs={"pk": 2})
    client.force_login(user)
    response = client.delete(url)
    assert response.status_code == 404, response.data


# UPDATE A QUOTE
def test_quote_update_with_auth(user, quote, client):
    """Authorized user updates a quote"""

    url = reverse("quote_update", kwargs={"pk": quote.id})
    client.force_login(user)
    data = {"quote_id": quote.id, "text": "UPDATED QUOTE", "comment": "UPDATED COMMENT"}
    response = client.put(url, data, content_type="application/json")
    assert response.status_code == 200, response.data


def test_quote_update_no_auth(quote, client):
    """Unauthorized user updates a quote"""

    url = reverse("quote_update", kwargs={"pk": quote.id})
    data = {"quote_id": quote.id, "text": "UPDATED QUOTE", "comment": "UPDATED COMMENT"}
    response = client.put(url, data)
    assert response.status_code == 403, response.data
    # TODO WHY SERVER RESPONDS FORBIDDEN 403 and not 401 which is Unauthorized?


def test_quote_update_no_quote(quote, user, client):
    """Authorized user updates a quote which doesn't exist in DB"""

    wrong_id = quote.id + 1
    url = reverse("quote_update", kwargs={"pk": wrong_id})
    client.force_login(user)
    data = {"quote_id": quote.id, "text": "UPDATED QUOTE", "comment": "UPDATED COMMENT"}
    response = client.put(url, data)
    assert response.status_code == 404, response.data


# GET A RANDOM QUOTE
def test_get_random_quote_with_auth(user, quote, client):
    """Authorized user retrieves a random quote"""

    url = reverse("random_quote")
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 204, response.data


def test_get_random_quote_no_auth(quote, client):
    """Unauthorized user retrieves a random quote"""

    url = reverse("random_quote")
    response = client.get(url)
    assert response.status_code == 403, response.data
    # TODO WHY SERVER RESPONDS FORBIDDEN 403 and not 401 which is Unauthorized?


def test_get_random_quote_404(user, client):
    """Authorized user retrieves a random quote which doesn't exist in DB"""

    url = reverse("random_quote")
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 404, response.data


# GET BY BOOK LIST
def test_get_by_book_list(user, books, client):
    """Authorized user retrieves a list of his books"""

    url = reverse("by_book")
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200, response.data
    assert len(response.data["results"]) == len(books)


def test_get_by_book_list_no_auth(books, client):
    """Unauthorized user retrieves a list of his books"""

    url = reverse("by_book")
    response = client.get(url)
    assert response.status_code == 403, response.data


# GET BOOK PAGE WITH LIST OF QUOTES
def test_get_book_page_quote_list(user, book, quotes, client):
    """Authorized user retrieves a list of quotes inside a book"""

    url = reverse("book_page", kwargs={"pk": book.id})
    client.force_login(user)
    response = client.get(url)
    print(f"{client=}")
    assert response.status_code == 200, response.data
    assert len(response.data) == len(quotes)


def test_get_book_page_quote_list_no_auth(book, quotes, client):
    """Unauthorized user retrieves a list of quotes inside a book"""

    url = reverse("book_page", kwargs={"pk": book.id})
    response = client.get(url)
    assert response.status_code == 403, response.data
