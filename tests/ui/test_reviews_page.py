import time
import allure
import pytest
from playwright.sync_api import sync_playwright
from conftest import browser
from  models.page_obj_models import CinescopeMoviesPage, CinescopeMoviePage, CinescopLoginPage

@allure.epic("Тестирование UI")
@allure.feature("Тестирование оставления отзывы")
@pytest.mark.ui

class TestWritingReview:
    @allure.title("Написание отзыва")
    def test_writing_review_by_user(self, logged_in_user_page):
        movie_page = CinescopeMoviePage(logged_in_user_page)
        movie_page.open()
        movie_page.writing_a_review("Отличный фильм, посмотрю еще раз")
        movie_page.select_rate("4")
        movie_page.click_review_button()

        movie_page.make_screenshot_and_attach_to_allure()
        movie_page.assert_review_pop_up()
