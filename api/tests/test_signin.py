from http.client import responses
import pytest
from django.urls import reverse

pytestmark = [pytest.mark.django_db]


def test_signin_success(user, client):
    url = reverse("account_login")
    data = {"email": "test@mail.com", "password": "1234pass!Wd"}
    response = client.post(url, data)
    print(response.cookies)
    assert response.status_code == 200


@pytest.mark.parametrize(
    ["email", "password", "status_code"],
    (
        ("test@mail.com", "7721pass!Wd", 400),
        ("test2@mail.com", "1234pass!Wd", 400),
    ),
)
def test_signin_fail(user, client, email, password, status_code):
    url = reverse("api_login")
    data = {"email": email, "password": password}
    response = client.post(url, data)
    print(response)
    assert response.status_code == status_code


# TODO update tests for API login/logout
