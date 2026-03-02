import allure
import pytest
from models.pydantic_model import (
    CreateMovieResponse,
    GetMoviesResponse,
    GetMovieResponse,
    EditMovieRequest,
)
from utils.data_generator import faker


@allure.epic("Тестирование Movies API")
@allure.feature("Тестирование раздела Фильмы")
class TestMoviesAPI:

    @pytest.mark.api
    @pytest.mark.db
    @allure.title("Получение всех фильмов GET /movies")
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
        with allure.step(
            "Positive-case: отправка запроса с query параметрами, и получение списка фильмов"
        ):
            response = super_admin.api.movies_api.get_movies(params)
            response_data = GetMoviesResponse(**response.json())
            assert response_data.pageSize == 10
            assert response_data.page == 1

        for movie in response_data.movies:
            assert movie.price >= min_price
            assert movie.price <= max_price
            assert movie.location == locations
            assert movie.published is True
            assert movie.genreId == genre_id

    @pytest.mark.api
    @pytest.mark.db
    @allure.title("Создание фильма POST /movies")
    def test_create_film(self, request_movies, super_admin, db_helper):
        with allure.step("Positive-case: создание фильма"):
            response = super_admin.api.movies_api.create_movie(request_movies)
            response_data = CreateMovieResponse(**response.json())
        assert response_data.name == request_movies.name
        assert response_data.price == request_movies.price
        assert response_data.description == request_movies.description
        assert response_data.location == request_movies.location
        assert response_data.published == request_movies.published
        assert response_data.genreId == request_movies.genreId

        with allure.step("Проверка наличия фильма в базе данных"):
            db_movie_check = db_helper.get_movie_by_id(response_data.id)
        assert db_movie_check.id == response_data.id
        assert db_movie_check.name == response_data.name
        assert db_movie_check.price == response_data.price

        with allure.step("Удаление данных c проверкой в БД"):
            super_admin.api.movies_api.delete_movie(response_data.id)
            db_delete_check = db_helper.get_movie_by_id(response_data.id)
            assert db_delete_check is None

    @pytest.mark.api
    @allure.title("Получение фильма GET /movies{id}")
    def test_get_movie(self, super_admin, created_film_with_cleanup, db_helper):
        with allure.step("Positive-case: получение информации о фильме"):
            movie_id = created_film_with_cleanup.id
            response = super_admin.api.movies_api.get_movie(movie_id)
            response_data = GetMovieResponse(**response.json())
        assert response_data.id == created_film_with_cleanup.id
        assert response_data.name == created_film_with_cleanup.name
        assert response_data.price == created_film_with_cleanup.price
        assert response_data.description == created_film_with_cleanup.description
        assert response_data.location == created_film_with_cleanup.location
        assert response_data.published == created_film_with_cleanup.published
        assert response_data.genreId == created_film_with_cleanup.genreId
        assert response_data.genre.name == created_film_with_cleanup.genre.name
        assert response_data.createdAt == created_film_with_cleanup.createdAt
        assert response_data.rating == created_film_with_cleanup.rating

    @pytest.mark.api
    @pytest.mark.db
    @allure.title("Редактирование фильма PATCH /movies{id}")
    def test_partial_update_movie(
        self, super_admin, created_film_with_cleanup, db_helper
    ):
        with allure.step("Positive-case: частичное изменение информации о фильме"):
            movie_id = created_film_with_cleanup.id
            movie_data = {"name": f"{faker.unique.word()}"}
            response = super_admin.api.movies_api.partial_update_movie(
                movie_id, movie_data
            )
            response_data = EditMovieRequest(**response.json())
        assert response_data.name == movie_data["name"]

        with allure.step("Проверка изменений в базе данных"):
            db_check_part_update = db_helper.get_movie_by_name(movie_data["name"])
        assert db_check_part_update.name == response_data.name

    @pytest.mark.parametrize(
        "role, expected_status",
        [("super_admin", 200), ("common_user", 403), ("admin", 403)],
    )
    @pytest.mark.slow
    @pytest.mark.api
    @allure.title("Удаление фильма DELETE /movies{id}")
    def test_delete_movie(
        self,
        role,
        created_film,
        expected_status,
        super_admin,
        common_user,
        admin,
        request,
    ):
        user = request.getfixturevalue(role)
        with allure.step("Positive case: Успешное удаление фильма"):
            movie_id = created_film.id
            response = user.api.movies_api.delete_movie(movie_id, expected_status)
        if expected_status == 200:
            response_data = CreateMovieResponse(**response.json())
            assert response_data.id == created_film.id
            assert response_data.name == created_film.name
            assert response_data.price == created_film.price
            assert response_data.description == created_film.description
            assert response_data.location == created_film.location
            assert response_data.published == created_film.published
            assert response_data.genreId == created_film.genreId
            assert response_data.genre.name == created_film.genre.name
            assert response_data.createdAt == created_film.createdAt
            assert response_data.rating == created_film.rating
        else:
            assert "Forbidden" in response.text

    @pytest.mark.api
    @allure.title("Неуспешное получение списка фильмов GET /movies")
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
        with allure.step(
            "Negative-case: отправка запроса с ошибочными query параметрами"
        ):
            response = super_admin.api.movies_api.get_movies(
                params, expected_status=400
            )
        assert "Bad Request" in response.text

    @pytest.mark.api
    @allure.title("Создание фильма с некорректным телом запроса POST /movies")
    def test_create_film_negative(self, super_admin):
        bad_request_movies = {
            "imageUrl": "https://image.url",
            "price": 100,
            "description": "Описание фильма",
            "location": "SPB",
            "published": "true",
            "genreId": 1,
        }
        with allure.step(
            "Negative-case: Отправка запроса c некорректными параметрами в теле"
        ):
            response = super_admin.api.movies_api.create_movie(
                bad_request_movies, expected_status=400
            )
        assert "Bad Request" in response.text

    @pytest.mark.api
    @allure.title("Получение несуществующего фильма GET /movies{id}")
    def test_get_movie_negative(self, super_admin):
        with allure.step(
            "Negative-case: попытка получения информации о несуществующем фильме"
        ):
            movie_id = faker.random_int(999999, 9999999, 10000)
            response = super_admin.api.movies_api.get_movie(
                movie_id, expected_status=404
            )
        assert "Not Found" in response.text

    @pytest.mark.api
    @allure.title("Редактирование несуществующего фильма PATCH /movies{id}")
    def test_partial_update_movie_negative(
        self, super_admin, created_film_with_cleanup
    ):
        with allure.step(
            "Negative-case: попытка изменить данные в несуществующем фильме"
        ):
            movie_id = faker.random_int(99999, 999999, 10000)
            movie_data = {"surname": f"{faker.unique.word()}"}
            response = super_admin.api.movies_api.partial_update_movie(
                movie_id, movie_data, expected_status=404
            )
        assert "Not Found" in response.text

    @pytest.mark.api
    @allure.title("Удаление несуществующего фильма DELETE /movies{id}")
    def test_delete_movie_negative(self, super_admin):
        with allure.step("Negative-case: Попытка удалить несуществующий фильм"):
            movie_id = faker.random_int(999999, 9999999, 10000)
            response = super_admin.api.movies_api.delete_movie(
                movie_id, expected_status=404
            )
        assert "Not Found" in response.text

    @pytest.mark.slow
    @pytest.mark.api
    @allure.title("Создание фильма под пользователем USER POST /movies")
    def test_create_movie_by_user_negative(self, common_user, request_movies):
        with allure.step("Negative-case: Попытка создать фильм под пользователем USER"):
            response = common_user.api.movies_api.create_movie(
                request_movies, expected_status=403
            )
        assert "Forbidden" in response.text

    @pytest.mark.db
    @allure.title("Создание фильма c проверкой в базе данных POST /movies")
    def test_create_film_with_database_check(
        self, request_movies, super_admin, db_helper
    ):
        with allure.step("Проверка отсутствия фильма с заданным именем в базе данных"):
            db_movie_check = db_helper.get_movie_by_name(request_movies.name)
        assert db_movie_check is None

        with allure.step("Отправка запроса на создание фильма"):
            response = super_admin.api.movies_api.create_movie(request_movies)
            response_data = CreateMovieResponse(**response.json())

        with allure.step("Проверка наличия созданного фильма в базе данных"):
            db_movie_check = db_helper.get_movie_by_name(request_movies.name)
        assert db_movie_check is not None

        assert db_movie_check.name == response_data.name
        assert db_movie_check.id == response_data.id
        assert db_movie_check.price == response_data.price

        with allure.step("Удаление фильма и проверка его отсутствия в базе данных"):
            super_admin.api.movies_api.delete_movie(response_data.id)
            db_movie_check = db_helper.get_movie_by_name(response_data.name)
        assert db_movie_check is None

    @pytest.mark.db
    @allure.title("Удаление фильма c проверкой в базе данных DELETE /movies/{id}")
    def test_delete_movie_with_database_check(
        self, super_admin, db_helper, request_movies_db
    ):
        with allure.step(
            "Генерация несуществующего movie_id и подготовка тестовых данных"
        ):
            movie_id = faker.random_int(999999, 9999999, 10000)
            get_movie_id = db_helper.get_movie_by_id(movie_id)

        if get_movie_id is None:
            movie_data = request_movies_db.copy()
            movie_data["id"] = movie_id
            db_helper.create_test_movie(movie_data)

        with allure.step("Отправка запроса на удаление фильма"):
            response = super_admin.api.movies_api.delete_movie(movie_id)

        with allure.step("Проверка удаления фильма из БД"):
            get_db_check = db_helper.get_movie_by_id(movie_id)
            assert get_db_check is None
