from playwright.sync_api import Page
from models.pages.base_page import BasePage

class CinescopeMoviesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}"

        self.profile_icon = "p[.text-sm]"
        self.profile_button = "button[type = 'button']"

        self.movies_titles = "h2[text() = 'Последние фильмы']"

        self.movie_description = "p[.mt-5 truncate]"
        self.movie_button = "a[href='/movies' and text()='Подробнее]'"

    def click_to_random_film(self):
        self.page.locator(self.movie_button).click()

    def assert_was_redirect_to_movie_page(self, movie_id: int):
        expected_url = f"{self.home_url}movies/{movie_id}"
        self.wait_redirect_for_url(expected_url)
