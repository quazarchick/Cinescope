import pytest
import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT


class TestAuthAPI:
    def test_register_user(self, test_user, api_manager):
        # URL для регистрации
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER не назначена у пользователя"

    def test_register_and_login_user(self, test_user, registered_user, api_manager):
        # Собираем УРЛ
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"],
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()
        assert "accessToken" in response_data, "accessToken отсутствует"
        assert (
            response_data["user"]["email"] == test_user["email"]
        ), "email записан некорректно"

    def test_delete_user(self, test_user, registered_user, api_manager):
        api_manager.auth_api.authenticate(
            (registered_user["email"], registered_user["password"])
        )

        response = api_manager.user_api.delete_user(registered_user["id"])
