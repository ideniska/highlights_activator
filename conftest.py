import pytest
from users.models import CustomUser
from rest_framework.authtoken.models import Token


@pytest.fixture
def user() -> CustomUser:
    # Create test user
    user = CustomUser.objects.create_user("test_user", "test@mail.com", "1234pass!Wd")
    return user


# Authorized client
@pytest.fixture
def api_client(client, user):
    token = Token.objects.create(user=user)
    client.defaults["HTTP_AUTHORIZATION"] = f"Token {token}"
    return client
