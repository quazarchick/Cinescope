"""
Фикстуры упрощают и автоматизируют подготовку данных и сессий для тестов. Мы создали:

1. `test_user` – генерация случайного пользователя.
2. `auth_session` – регистрация, логин и создание авторизационной сессии.
"""

import requests
import pytest
from utils.data_generator import DataGenerator
from clients.api_manager import ApiManager
from resources.user_creds import SuperAdminCreds
from entities.user import User
from constants.roles import Roles
from models.pydantic_model import TestUser, RegisterUserResponse


@pytest.fixture()
def test_user():
    """
    Генерация случайного пользователя для тестов
    """
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture()
def test_admin():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.ADMIN.value],
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
    response = api_manager.auth_api.register_user(test_user)
    response_data = RegisterUserResponse(**response.json())
    registered_user = test_user.copy()
    registered_user.email = response_data.email
    response_data.password = registered_user.password
    return response_data


@pytest.fixture()
def created_film_with_cleanup(super_admin, request_movies):
    # Positive-case: создание фильма
    response = super_admin.api.movies_api.create_movie(request_movies)
    movie_data = response.json()
    assert movie_data["id"] is not None
    movie_id = movie_data["id"]
    yield movie_data

    response_delete = super_admin.api.movies_api.delete_movie(movie_id)
    response_get = super_admin.api.movies_api.get_movie(movie_id, expected_status=404)


@pytest.fixture()
def created_film(super_admin, request_movies):
    response = super_admin.api.movies_api.create_movie(request_movies)
    movie_data = response.json()
    assert movie_data["id"] is not None
    movie_id = movie_data["id"]
    return movie_data


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


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session,
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.model_copy(update={"verified": True, "banned": False})
    return updated_data

@pytest.fixture(scope="function")
def creation_admin_data(test_admin):
    updated_data = test_admin.copy()
    updated_data.update({"verified": True, "banned": False})
    return updated_data


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session,
    )

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin(user_session, super_admin, creation_admin_data):
    new_session = user_session()

    admin = User(
        creation_admin_data["email"],
        creation_admin_data["password"],
        [Roles.ADMIN.value],
        new_session
    )

    super_admin.api.user_api.create_user(creation_admin_data)
    admin.api.auth_api.authenticate(admin.creds)
    return admin