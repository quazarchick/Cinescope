import allure
from playwright.sync_api import Page
from models.pages.page_action import PageAction

class BasePage(PageAction):
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_url = "https://dev-cinescope.coconutqa.ru/"

        self.home_button = "a[href=/ and text()= 'Cinescope']"
        self.all_movies_button = "a[href='/movies' and text()='Все фильмы']"

    @allure.step("Переход на главную страницу, из шапки сайта")
    def go_to_home_page(self):
        self.click_element(self.home_button)
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Переход на страницу 'Все фильмы, из шапки сайта'")
    def go_to_all_movies(self):
        self.page.click(self.all_movies_button)
        self.page.wait_for_url(f"{self.home_url}movies")