from models.pydantic_model import RegisterUserResponse


class TestAuthAPI:
    def test_register_user(self, test_user, api_manager):
        # URL для регистрации
        response = api_manager.auth_api.register_user(test_user)
        response_data = RegisterUserResponse(**response.json())
        assert response_data.email == test_user.email, "Email не совпадает"

    def test_register_and_login_user(self, test_user, registered_user, api_manager):
        # Собираем УРЛ
        login_data = {
            "email": registered_user.email,
            "password": registered_user.password,
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()
        assert (
            response_data["user"]["email"] == registered_user.email
        ), "email записан некорректно"
