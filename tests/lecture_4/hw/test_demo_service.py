import pytest
from starlette.testclient import TestClient

from http import HTTPStatus
from datetime import datetime
from pydantic import SecretStr
from typing import Any, Tuple

from lecture_4.demo_service.api.main import create_app
from lecture_4.demo_service.api.contracts import RegisterUserRequest, UserResponse, UserAuthRequest, SecretStr
from lecture_4.demo_service.core.users import UserInfo, UserService, UserEntity, UserRole, password_is_longer_than_8


demo_service = create_app()
demo_service.state.user_service = UserService()
client = TestClient(demo_service)


# register users for testing
def register_user(query: dict[str, Any]) -> RegisterUserRequest:
    user = RegisterUserRequest(
        username = query['username'],
        name = query['name'],
        birthdate = query['birthdate'],
        password = query['password']
    )

    return user


@pytest.mark.parametrize(
    "query", 
    [
        ({"username": "Laitielly",
          "name": "Anna",
          "birthdate": datetime.strptime('Jul 22 2002', '%b %d %Y'),
          "password": SecretStr("super_secret")
         }),
         ({"username": "Hahaha",
          "name": "Bob",
          "birthdate": datetime.strptime('May 05 2012', '%b %d %Y'),
          "password": SecretStr("hard_password_1234")
         })
    ],
)
def test_correct_register(query: dict) -> None:
    user = register_user(query)

    assert user.username == query['username']
    assert user.name == query['name']
    assert user.birthdate == query['birthdate']
    assert user.password == query['password']


# contract
def user_auth_request(query: dict) -> UserAuthRequest:
    user_auth = UserAuthRequest(
                    username = query['username'],
                    password = query['password']
                )

    return user_auth


@pytest.mark.parametrize(
    "query", 
    [
        ({"username": "Igor",
          "password": SecretStr("super_secret_yoy")
         }),
         ({"username": "Hihi-Haha",
          "password": SecretStr("kloyn")
         })
    ],
)
def test_correct_user_auth_request(query: dict) -> None:
    user = user_auth_request(query)

    assert user.username == query['username']
    assert user.password == query['password']


@pytest.fixture(scope='module')
def client():
    demo_app = create_app()
    demo_app.state.user_service = UserService()
    with TestClient(demo_app) as client:
        yield client


@pytest.mark.parametrize(
    ("json", "status"), 
    [
        ({"username": "Papapap",
          "name": "Vanya",
          "birthdate": '2024-04-24',
          "password": "super_secret123"
         }, HTTPStatus.OK),
         ({"username": "gouse",
          "name": "Vika",
          "birthdate": '2012-05-05',
          "password": "hard_password_1234"
         }, HTTPStatus.OK),
         ({"username": "chipi-chipi",
          "name": "chapa chapa",
          "birthdate": '2012-06-05',
          "password": "keklol"
         }, HTTPStatus.BAD_REQUEST),
         ({"username": "gouse",
          "name": "Vika",
          "birthdate": '2012-05-05',
          "password": "hard_password_1234"
         }, HTTPStatus.BAD_REQUEST),
    ],
)
def test_user_register(client, json: dict, status) -> None:
    response = client.post(
        '/user-register',
        json=json,
    )
    
    expected_json = {
        "username": json["username"],
        "name": json["name"],
        "role": "user",
        "birthdate": json["birthdate"] + "T00:00:00",
        "uid": response.json().get("uid")
    }
    
    assert response.status_code == status

    if response.status_code == HTTPStatus.OK:
        assert response.json() == expected_json


@pytest.mark.parametrize(
    ("params", "auth", "status"), 
    [
        ({'id': 2}, ('Papapap', 'super_secret123'), HTTPStatus.OK),
        ({'id': 2, "username": 'Papapap'}, 
        ('Papapap', 'super_secret123'), HTTPStatus.BAD_REQUEST),
        ({}, 
        ('Papapap', 'super_secret123'), HTTPStatus.BAD_REQUEST),
        ({'id': 2}, None, HTTPStatus.UNAUTHORIZED),
        ({"username": 'Papapap'}, ('Papapap', 'super_secret123'),
        HTTPStatus.OK),
        ({"id": 999}, ('Papapap', 'super_secret123'),
        HTTPStatus.NOT_FOUND)
    ],
)
def test_user_get_by_uid(client, params: dict, auth: Tuple, status):
    response = client.post(
        '/user-get',
        params=params,
        auth=auth
    )
    assert response.status_code == status, (
        f'Expected status {status}, but got {response.status_code}'
    )


@pytest.mark.parametrize(
    ("params", "auth", "status"), 
    [
        ({'id': 2}, ('admin', 'superSecretAdminPassword123'), HTTPStatus.OK),
        ({'id': 1}, ('gouse', 'hard_password_1234'), HTTPStatus.FORBIDDEN), 
        ({'id': 1}, ('egor', 'hard_password_1234'), HTTPStatus.UNAUTHORIZED),
        ({'id': 100}, ('admin', 'superSecretAdminPassword123'), HTTPStatus.BAD_REQUEST)
    ],
)
def test_user_promote(client, params, auth, status):
    response = client.post(
        '/user-promote',
        params=params,
        auth=auth
    )
    assert response.status_code == status, (
        f'Expected status {status}, but got {response.status_code}'
    )


