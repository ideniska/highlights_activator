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
