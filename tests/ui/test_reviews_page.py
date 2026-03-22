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
    def test_writing_review_by_super_admin(self, super_admin):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()
            login_page = CinescopLoginPage(page)

            login_page.open()
            login_page.login(super_admin.email, super_admin.password)

            login_page.wait_redirect_to_homepage()
            login_page.make_screenshot_and_attach_to_allure()
            login_page.assert_allert_was_pop_up()

            movies_page = CinescopeMoviesPage(page)
            movies_page.click_to_random_film()

            movie_page = CinescopeMoviePage(page)
            movie_page.writing_a_review("Фильм понравился, но могли бы чё получше придумать")
            movie_page.assert_review_pop_up()