from playwright.sync_api import Page
from models.pages.base_page import BasePage

class CinescopeLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}login"

        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"

        self.login_button = "button[type='submit']"
        self.register_button = "a[href='/register' and text()='Зарегистрироваться']"

    def open_login_url(self):
        self.open_url(self.url)

    def login(self, email: str, password: str):
        self.enter_text_to_element(self.email_input, email)
        self.enter_text_to_element(self.password_input, password)
        self.click_element(self.login_button)

    def assert_was_redirect_to_home_page(self):
        self.wait_redirect_for_url(self.home_url)

    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Вы вошли в аккаунт")

