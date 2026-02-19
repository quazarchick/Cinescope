import pytest
from clients import api_manager
from models.pydantic_model import RegisterUserResponse


class TestUser:
    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)
        response_data = RegisterUserResponse(**response.json())
        assert response_data.email == creation_user_data.email
        assert response_data.fullName == creation_user_data.fullName
        assert response_data.roles == creation_user_data.roles
        assert response_data.verified == creation_user_data.verified
        assert response_data.banned == creation_user_data.banned

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data)
        create_user_response_data = RegisterUserResponse(**created_user_response.json())
        get_by_id = super_admin.api.user_api.get_user(create_user_response_data.id)
        response_by_id = RegisterUserResponse(**get_by_id.json())
        get_by_email = super_admin.api.user_api.get_user(
            create_user_response_data.email
        )
        response_by_email = RegisterUserResponse(**get_by_email.json())

        assert (
            response_by_id == response_by_email
        ), "Содержание ответов должно быть идентичным"
        assert response_by_id.email == creation_user_data.email, "Email не совпадает"
        assert (
            response_by_id.fullName == creation_user_data.fullName
        ), "ФИО не совпадает"
        assert response_by_id.roles == creation_user_data.roles, "Роль не совпадает"

    def test_delete_user(self, super_admin, creation_user_data):
        creation_user = super_admin.api.user_api.create_user(creation_user_data)
        response_creation_user = RegisterUserResponse(**creation_user.json())
        delete_user = super_admin.api.user_api.delete_user(response_creation_user.id)
        repeat_delete_user = super_admin.api.user_api.delete_user(
            response_creation_user.id, expected_status=404
        )

    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)
