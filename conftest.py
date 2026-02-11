"""
Фикстуры упрощают и автоматизируют подготовку данных и сессий для тестов. Мы создали:

1. `test_user` – генерация случайного пользователя.
2. `auth_session` – регистрация, логин и создание авторизационной сессии.
"""

import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
import pytest
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from clients.api_manager import ApiManager


@pytest.fixture()
def test_user():
    """
    Генерация случайного пользователя для тестов
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"],
    }


@pytest.fixture()
def request_movies():
    random_filmname = DataGenerator.generate_random_filmname()
    random_price = DataGenerator.generate_random_price()
    random_description = DataGenerator.generate_random_description()
    random_location = DataGenerator.generate_random_location()
    random_published = DataGenerator.generate_random_published()
    random_genre = DataGenerator.generate_random_genre()

    return {
        "name": random_filmname,
        "imageUrl": "https://image.url",
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": random_published,
        "genreId": random_genre,
    }


@pytest.fixture()
def registered_user(api_manager, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = api_manager.user_api.send_request(test_user)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user


@pytest.fixture()
def created_film_with_cleanup(api_manager, admin_credentials, request_movies):
    api_manager.auth_api.authenticate(
        (admin_credentials["username"], admin_credentials["password"])
    )

    # Positive-case: создание фильма
    response = api_manager.movies_api.create_movie(request_movies)
    movie_data = response.json()
    assert movie_data["id"] is not None
    movie_id = movie_data["id"]
    yield movie_data
    api_manager.auth_api.authenticate(
        (admin_credentials["username"], admin_credentials["password"])
    )

    response_delete = api_manager.movies_api.delete_movie(movie_id)
    response_get = api_manager.movies_api.get_movie(movie_id, expected_status=404)

@pytest.fixture()
def created_film(api_manager, admin_credentials, request_movies):
    api_manager.auth_api.authenticate(
        (admin_credentials["username"], admin_credentials["password"])
    )

    response = api_manager.movies_api.create_movie(request_movies)
    movie_data = response.json()
    assert movie_data["id"] is not None
    movie_id = movie_data["id"]
    return movie_data

@pytest.fixture(scope="session")
def admin_credentials():
    return {"username": "api1@gmail.com", "password": "asdqwe123Q"}


@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@pytest.fixture(scope="session")
def authorized_admin_session(api_manager, admin_credentials):
    api_manager.auth_api.authenticate(
        (admin_credentials["username"], admin_credentials["password"])
    )
    return api_manager
