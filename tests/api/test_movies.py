from itertools import count

import pytest
import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from utils.data_generator import faker


class TestMoviesAPI:
    def test_get_movie_posters(self, api_manager):
        params = {
            "pageSize": 10,
            "page": 1,
            "minPrice": 1,
            "maxPrice": 1000,
            "locations": "MSK",
            "published": "true",
            "genreId": 1,
            "createdAt": "asc",
        }
        # Positive-case: отправка запроса с query параметрами, и получение списка постеров
        response = api_manager.movies_api.get_movie_posters(params)
        response_data = response.json()
        assert response_data["pageSize"] == 10
        assert response_data["page"] == 1
        assert len(response_data["movies"]) <= 10
        for movie in response_data["movies"]:
            assert movie["price"] >= 1
            assert movie["price"] <= 1000
            assert movie["location"] == "MSK"
            assert movie["published"] is True
            assert movie["genreId"] == 1

    def test_create_film(self, request_movies, admin_credentials, api_manager):
        api_manager.auth_api.authenticate(
            (admin_credentials["username"], admin_credentials["password"])
        )

        # Positive-case: создание фильма
        response = api_manager.movies_api.create_film(request_movies)
        response_data = response.json()
        assert response_data["id"] is not None
        assert response_data["name"] == request_movies["name"]
        assert response_data["price"] == request_movies["price"]
        assert response_data["description"] == request_movies["description"]
        assert response_data["location"] == request_movies["location"]
        assert response_data["published"] == request_movies["published"]
        assert response_data["genreId"] == request_movies["genreId"]
        assert response_data["genre"]["name"] is not None
        assert response_data["createdAt"] is not None
        assert response_data["rating"] is not None

    def test_get_movie(self, api_manager, created_film):
        # Positive-case: получение информации о фильме
        movie_id = created_film["id"]
        response = api_manager.movies_api.get_movie(movie_id)
        response_data = response.json()
        assert response_data["id"] == created_film["id"]
        assert response_data["name"] == created_film["name"]
        assert response_data["price"] == created_film["price"]
        assert response_data["description"] == created_film["description"]
        assert response_data["location"] == created_film["location"]
        assert response_data["published"] == created_film["published"]
        assert response_data["genreId"] == created_film["genreId"]
        assert response_data["genre"]["name"] == created_film["genre"]["name"]
        assert response_data["createdAt"] == created_film["createdAt"]
        assert response_data["rating"] == created_film["rating"]

    def test_partial_update_movie(self, api_manager, created_film, admin_credentials):
        api_manager.auth_api.authenticate(
            (admin_credentials["username"], admin_credentials["password"])
        )

        # Positive-case: частичное изменение информации о фильме
        movie_id = created_film["id"]
        movie_data = {"name": f"{faker.unique.word()}"}
        response = api_manager.movies_api.partial_update_movie(movie_id, movie_data)
        response_data = response.json()
        assert response_data["name"] == movie_data["name"]

    def test_delete_movie(self, api_manager, admin_credentials, created_film):
        # Positive: Успешное удаление фильма
        movie_id = created_film["id"]
        response = api_manager.movies_api.delete_movie(movie_id)
        response_data = response.json()
        assert response_data["id"] == created_film["id"]
        assert response_data["name"] == created_film["name"]
        assert response_data["price"] == created_film["price"]
        assert response_data["description"] == created_film["description"]
        assert response_data["location"] == created_film["location"]
        assert response_data["published"] == created_film["published"]
        assert response_data["genreId"] == created_film["genreId"]
        assert response_data["genre"]["name"] == created_film["genre"]["name"]
        assert response_data["createdAt"] == created_film["createdAt"]
        assert response_data["rating"] == created_film["rating"]
