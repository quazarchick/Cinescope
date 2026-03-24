import time
import allure
import pytest
from playwright.sync_api import sync_playwright
from models.pages.login_page import CinescopeLoginPage

@allure.epic("Тестирование UI")
@allure.feature("Тестирование страницы Login")
@pytest.mark.ui
class TestLoginPage:
    @allure.title("Проведение успешного входа в систему")
    def test_login_by_ui(self, registered_user):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()
            login_page = CinescopeLoginPage(page)

            login_page.open_login_url()
            login_page.login(registered_user.email, registered_user.password)

            login_page.wait_redirect_for_url()
            login_page.make_screenshot_and_attach_to_allure()
            login_page.assert_allert_was_pop_up()

            time.sleep(5)
            browser.close()