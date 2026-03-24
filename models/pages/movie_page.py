from playwright.sync_api import Page
from models.pages.base_page import BasePage

class CinescopeMoviePage(BasePage):
    def __init__(self, page: Page, created_film_with_cleanup):
        super().__init__(page)
        self.movie_title = created_film_with_cleanup.name
        self.movie_id = created_film_with_cleanup.id
        self.movie_url = f"{self.home_url}movies/{self.movie_id}"

        self.reviews_title = "h2[text() = 'Отзывы:']"
        self.reviews_text = "textarea[name = 'text']"
        self.buy_button = "a[href = '/payment?movieId=']"
        self.review_rate = page.get_by_text("Оценка:").locator("..").get_by_role("combobox")
        self.review_submit_button = "button[type = 'submit']"

    def open_movie_url(self):
        self.open_url(self.movie_url)

    def writing_a_review(self, text_review: str):
        self.enter_text_to_element(self.reviews_text, text_review)

    def select_rate(self, rate):
        self.review_rate.click()
        self.page.get_by_role("option", name=rate).click()

    def click_review_button(self):
        self.click_element(self.review_submit_button)

    def assert_review_pop_up(self):
        self.check_pop_up_element_with_text("Отзыв успешно создан")