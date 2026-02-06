import pytest
import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPONT

class TestAuthAPI:
    def test_register_user(self, test_user):
        #URL для регистрации
        register_url = f"{BASE_URL}{REGISTER_ENDPONT}"

        #Отправка запроса на регистрацию
        response = requests.post(register_url, json=test_user, headers=HEADERS)

        #Логирование ответа для диагностики
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        #Проверки
        assert response.status_code == 201, "Ошибка регистрации пользователя"
        response_data = response.json()
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"

        #Проверяем, что роль USER назначена по умолчанию




