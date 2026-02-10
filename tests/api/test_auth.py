import pytest
import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPONT, LOGIN_ENDPOINT

class TestAuthAPI:
    def test_register_user(self, test_user, requester):
        #URL для регистрации
        response = requester.send_request(
            method="POST",
            endpoint=REGISTER_ENDPONT,
            data=test_user,
            expected_status=201
        )
        response_data = response.json()
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER не назначена у пользователя"

    def test_register_and_login_user(self, test_user, registered_user, requester):
        #Собираем УРЛ
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = requester.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status = 200
        )
        response_data = response.json()
        assert "accessToken" in response_data, "accessToken отсутствует"
        assert response_data["user"]["email"] == test_user["email"], "email записан некорректно"

        #Авторизация с некорректным паролем
        pswd_fail_data = {
            "email":registered_user["email"],
            "password": "password"
        }
        #Отправляем запрос
        response = requester.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=pswd_fail_data,
            expected_status=401
        )
        response_data = response.json()
        assert response_data["message"] == "Неверный логин или пароль", "Текста нет"

        # Авторизация с некорректным email
        email_fail_data = {
            "email": "email@mail.com",
            "password": registered_user["password"]
        }
        response = requester.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=email_fail_data,
            expected_status=401
        )
        response_data = response.json()
        assert response_data["message"] == "Неверный логин или пароль", "Текста нет"

        #Авторизация с пустым телом запроса
        response = requester.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data={},
            expected_status=401
        )
        response_data = response.json()
        assert response_data["message"] == "Неверный логин или пароль", "Текста нет"



