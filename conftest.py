'''
Фикстуры упрощают и автоматизируют подготовку данных и сессий для тестов. Мы создали:

1. `test_user` – генерация случайного пользователя.
2. `auth_session` – регистрация, логин и создание авторизационной сессии.
'''
from multiprocessing.resource_tracker import register

import requests
from requests import session

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
        "roles": ["USER"]
    }

@pytest.fixture()
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method = "POST",
        endpoint = REGISTER_ENDPOINT,
        data = test_user,
        expected_status = 201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

    '''- Создает объект `requests.Session`, который используется всеми API-классами.
        - Гарантирует, что сессия будет корректно закрыта после завершения всех тестов.'''

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


    '''- Инициализирует `ApiManager` с общей сессией.
        - Позволяет тестам централизованно обращаться ко всем API-классам через объект `api_manager`.
        - Используем **ApiManager** в фикстуре Pytest для обеспечения доступа к API классам в тестах:
        Фикстура **api_manager** предоставляет тестам единый интерфейс для работы с различными API, используя одну и ту же сессию.'''