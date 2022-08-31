import pytest
from users.models import CustomUser


@pytest.fixture
def user() -> CustomUser:
    # Create test user
    user = CustomUser.objects.create_user("test_user", "test@mail.com", "1234pass!Wd")
    # login()
    return user


# auth
# create token = obtain token
