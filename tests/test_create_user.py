import pytest

from rest_framework import status
from django.test.client import Client
from django.contrib.auth import get_user_model

User = get_user_model()


# @pytest.fixture
# def john() -> str:
#     return "John"


# def strange_calculator(a: int, b: int) -> int:
#     if a > b:
#         return a + b
#     else:
#         return a - b


# @pytest.mark.parametrize(
#     "a,b,expected",
#     [
#         (20, 10, 30),
#         (10, 20, -10),
#     ],
# )
# def test_user_creation_success(a: int, b: int, expected: int):
#     assert strange_calculator(a, b) == expected


@pytest.mark.django_db
def test_user_creation_success(client: Client):
    payload = {
        "email": "john@email.com",
        "password": "@Dm1n#LKJ",
        "first_name": "John",
        "last_name": "Doe",
    }

    response = client.post(path="/users/", data=payload)

    user: User = User.objects.get(id=1)

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert user.first_name == payload["first_name"]
