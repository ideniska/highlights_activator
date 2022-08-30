import pytest
from users.models import CustomUser

pytestmark = [pytest.mark.django_db]


def test_user_create(user):
    assert CustomUser.objects.count() == 1
