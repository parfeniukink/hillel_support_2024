import requests


def test_user_creation_success():
    url = "http://localhost:8000/users"

    payload = {
        "email": "john@email.com",
        "password": "@Dm1n#LKJ",
        "first_name": "John",
        "last_name": "Doe",
    }

    response = requests.post(url, json=payload)

    assert response.status_code == 201

