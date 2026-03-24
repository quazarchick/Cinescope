import allure
import pytest
from models.pages.movie_page import CinescopeMoviePage
from utils.data_generator import DataGenerator


@allure.epic("Тестирование UI")
@allure.feature("Тестирование оставления отзывы")
@pytest.mark.ui

class TestWritingReview:
    @allure.title("Написание отзыва")
    def test_writing_review_by_user(self, logged_in_user_page, created_film_with_cleanup):
        movie_page = CinescopeMoviePage(logged_in_user_page, created_film_with_cleanup)
        movie_page.open_movie_url()
        movie_page.writing_a_review("Отличный фильм, посмотрю еще раз")
        movie_page.select_rate(DataGenerator.generate_random_rate())
        movie_page.click_review_button()

        movie_page.assert_review_pop_up()
        movie_page.make_screenshot_and_attach_to_allure()
