import pytest
from conftest import super_admin, common_user
from utils.data_generator import faker


class TestMoviesAPI:

    @pytest.mark.parametrize(
        "min_price,max_price,locations,genre_id",
        [(1, 100, "MSK", 1), (100, 500, "SPB", 2)],
    )
    def test_get_movie_posters(
        self, super_admin, min_price, max_price, locations, genre_id
    ):
        params = {
            "pageSize": 10,
            "page": 1,
            "minPrice": min_price,
            "maxPrice": max_price,
            "locations": locations,
            "published": "true",
            "genreId": genre_id,
            "createdAt": "asc",
        }
        # Positive-case: отправка запроса с query параметрами, и получение списка постеров
        response = super_admin.api.movies_api.get_movies(params)
        response_data = response.json()
        assert response_data["pageSize"] == 10
        assert response_data["page"] == 1
        assert len(response_data["movies"]) <= 10
        for movie in response_data["movies"]:
            assert movie["price"] >= min_price
            assert movie["price"] <= max_price
            assert movie["location"] == locations
            assert movie["published"] is True
            assert movie["genreId"] == genre_id

    def test_create_film(self, request_movies, super_admin):
        # Positive-case: создание фильма
        response = super_admin.api.movies_api.create_movie(request_movies)
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

    def test_get_movie(self, super_admin, created_film_with_cleanup):
        # Positive-case: получение информации о фильме
        movie_id = created_film_with_cleanup["id"]
        response = super_admin.api.movies_api.get_movie(movie_id)
        response_data = response.json()
        assert response_data["id"] == created_film_with_cleanup["id"]
        assert response_data["name"] == created_film_with_cleanup["name"]
        assert response_data["price"] == created_film_with_cleanup["price"]
        assert response_data["description"] == created_film_with_cleanup["description"]
        assert response_data["location"] == created_film_with_cleanup["location"]
        assert response_data["published"] == created_film_with_cleanup["published"]
        assert response_data["genreId"] == created_film_with_cleanup["genreId"]
        assert (
            response_data["genre"]["name"] == created_film_with_cleanup["genre"]["name"]
        )
        assert response_data["createdAt"] == created_film_with_cleanup["createdAt"]
        assert response_data["rating"] == created_film_with_cleanup["rating"]

    def test_partial_update_movie(self, super_admin, created_film_with_cleanup):
        # Positive-case: частичное изменение информации о фильме
        movie_id = created_film_with_cleanup["id"]
        movie_data = {"name": f"{faker.unique.word()}"}
        response = super_admin.api.movies_api.partial_update_movie(movie_id, movie_data)
        response_data = response.json()
        assert response_data["name"] == movie_data["name"]


    def test_delete_movie(self, super_admin, created_film):
        # Positive: Успешное удаление фильма
        movie_id = created_film["id"]
        response = super_admin.api.movies_api.delete_movie(movie_id)
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

    def test_get_movie_posters_negative(self, super_admin):
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
        response = super_admin.api.movies_api.get_movies(params, expected_status=400)
        assert "Bad Request" in response.text

    def test_create_film_negative(self, super_admin):
        bad_request_movies = {
            "imageUrl": "https://image.url",
            "price": 100,
            "description": "Описание фильма",
            "location": "SPB",
            "published": "true",
            "genreId": 1,
        }
        # Negative-case: создание фильма c некорректными параметрами в теле запроса
        response = super_admin.api.movies_api.create_movie(
            bad_request_movies, expected_status=400
        )
        assert "Bad Request" in response.text

    def test_get_movie_negative(self, super_admin):
        # Negative-case: попытка получения информации о несуществующем фильме
        movie_id = faker.random_int(999999, 9999999, 10000)
        response = super_admin.api.movies_api.get_movie(movie_id, expected_status=404)
        assert "Not Found" in response.text

    def test_partial_update_movie_negative(
        self, super_admin, created_film_with_cleanup
    ):
        # Negative-case: попытка изменить данные в несуществующем фильме
        movie_id = created_film_with_cleanup["id"]
        movie_data = {"surname": f"{faker.unique.word()}"}
        response = super_admin.api.movies_api.partial_update_movie(
            movie_id, movie_data, expected_status=404
        )
        assert "Not Found" in response.text

    def test_delete_movie_negative(self, super_admin):
        # Negative-case: Попытка удалить несуществующий фильм
        movie_id = faker.random_int(999999, 9999999, 10000)
        response = super_admin.api.movies_api.delete_movie(
            movie_id, expected_status=404
        )
        response_data = response.json()
        assert "Not Found" in response.text

    def test_create_movie_by_user_negative(self, common_user, request_movies):
        # Negative-case: Попытка создать фильм под пользователем
        response = common_user.api.movies_api.create_movie(
            request_movies, expected_status=403
        )
        assert "Forbidden" in response.text

    @pytest.mark.parametrize("role, expected_status", [("super_admin", 200), ("common_user", 403), ("admin", 403)])
    def test_delete_movie_second(self, role, created_film, expected_status, super_admin, common_user, admin, request):
        user = request.getfixturevalue(role)
        # Positive: Успешное удаление фильма
        movie_id = created_film["id"]
        response = user.api.movies_api.delete_movie(movie_id, expected_status)
        response_data = response.json()
        if response.status_code == 200:
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
        else:
            assert "Forbidden" in response.text
