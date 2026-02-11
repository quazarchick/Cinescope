import pytest
import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from utils.data_generator import faker


class TestMoviesAPI:
    def test_get_movie_posters(self, authorized_admin_session):
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
        response = authorized_admin_session.movies_api.get_movies(params)
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

    def test_create_film(self, request_movies, authorized_admin_session):
        # Positive-case: создание фильма
        response = authorized_admin_session.movies_api.create_movie(request_movies)
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

    def test_get_movie(self, authorized_admin_session, created_film):
        # Positive-case: получение информации о фильме
        movie_id = created_film["id"]
        response = authorized_admin_session.movies_api.get_movie(movie_id)
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

    def test_partial_update_movie(self, authorized_admin_session, created_film):
        # Positive-case: частичное изменение информации о фильме
        movie_id = created_film["id"]
        movie_data = {"name": f"{faker.unique.word()}"}
        response = authorized_admin_session.movies_api.partial_update_movie(
            movie_id, movie_data
        )
        response_data = response.json()
        assert response_data["name"] == movie_data["name"]

    def test_delete_movie(self, authorized_admin_session, created_film):
        # Positive: Успешное удаление фильма
        movie_id = created_film["id"]
        response = authorized_admin_session.movies_api.delete_movie(movie_id)
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

    def test_get_movie_posters_negative(self, authorized_admin_session):
        params = {
            "pageSize": 10,
            "page": 1,
            "minPrice": 1,
            "maxPrice": 1000,
            "locations": "NNO",
            "published": "true",
            "genreId": 1,
            "createdAt": "asc",
        }
        # Negative-case: отправка запроса с ошибочными query параметрами
        response = authorized_admin_session.movies_api.get_movies(
            params, expected_status=400
        )
        assert "Bad Request" in response.text

    def test_create_film_negative(self, request_movies, authorized_admin_session):
        bad_request_movies = {
            "imageUrl": "https://image.url",
            "price": 100,
            "description": "Описание фильма",
            "location": "SPB",
            "published": "true",
            "genreId": 1,
        }
        # Negative-case: создание фильма c некорректными параметрами в теле запроса
        response = authorized_admin_session.movies_api.create_movie(
            bad_request_movies, expected_status=400
        )
        assert "Bad Request" in response.text

    def test_get_movie_negative(self, authorized_admin_session):
        # Negative-case: попытка получения информации о несуществующем фильме
        movie_id = faker.random_int(999999, 9999999,10000)
        response = authorized_admin_session.movies_api.get_movie(
            movie_id, expected_status=404
        )
        assert "Not Found" in response.text

    def test_partial_update_movie_negative(
        self, authorized_admin_session, created_film
    ):
        # Negative-case: попытка отправить несуществующий параметр в теле запроса для обновления информации
        movie_id = created_film["id"]
        movie_data = {"surname": f"{faker.unique.word()}"}
        response = authorized_admin_session.movies_api.partial_update_movie(
            movie_id, movie_data, expected_status=400
        )
        assert "Bad Request" in response.text

    def test_delete_movie_negative(self, authorized_admin_session):
        # Negative-case: Попытка удалить несуществующий фильм
        movie_id = faker.random_int(999999, 9999999,10000)
        response = authorized_admin_session.movies_api.delete_movie(
            movie_id, expected_status=404
        )
        response_data = response.json()
        assert "Not Found" in response.text
