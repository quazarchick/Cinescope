'''
Фикстуры упрощают и автоматизируют подготовку данных и сессий для тестов. Мы создали:

1. `test_user` – генерация случайного пользователя.
2. `auth_session` – регистрация, логин и создание авторизационной сессии.
'''
from multiprocessing.resource_tracker import register

import requests
from requests import session

from constants import BASE_URL, HEADERS, REGISTER_ENDPONT, LOGIN_ENDPOINT
import pytest
from utils.data_generator import DataGenerator

@pytest.fixture(scope="session")
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

    @pytest.fixture(scope="session")
    def auth_session(test_user):
        # Регистрируем нового пользователя
        register_url = f"{BASE_URL}{REGISTER_ENDPONT}"
        response = requests.post(register_url, json=test_user, headers=HEADERS)
        assert response.status_code == 201, "Ошибка регистрации полььзователя"

        #Логинимся для получения токена
        login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
        login_data = {
            "email":test_user["email"],
            "password": test_user["password"]
        }
        response = requests.post(login_url, json=login_data, headers=HEADERS)
        assert response.status_code == 200, "Ошибка авторизации"

        #Получаем токен и создаем сессию
        token = response.json().get("accessToken")
        assert token is not None, "Токен доступа отсутствует в ответе"

        session = requests.Session()
        session.headers.update(HEADERS)
        session.headers.update({"Autorization": f"Bearer {token}"})
        return session

