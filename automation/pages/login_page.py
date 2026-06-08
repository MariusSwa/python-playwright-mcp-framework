from playwright.sync_api import Page

from core.base_page import BasePage


class LoginPage(BasePage):

    # -------------------------
    # Page setup
    # -------------------------

    PAGE_HEADER = "Login"

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self, base_url: str) -> None:
        self.goto(base_url)

    # -------------------------
    # Locators
    # -------------------------

    EMAIL_INPUT = {
        "type": "label",
        "value": "Email"
    }

    PASSWORD_INPUT = {
        "type": "label",
        "value": "Password"
    }

    REMEMBER_ME = {
        "type": "role",
        "role": "checkbox",
        "name": "Remember Me"
    }

    LOGIN_BUTTON = {
        "type": "role",
        "role": "button",
        "name": "Login"
    }

    SUCCESS_MESSAGE = {
        "type": "text",
        "value": "Login successful"
    }

    ERROR_MESSAGE = {
        "type": "test_id",
        "value": "login-message",
    }

    # -------------------------
    # Actions
    # -------------------------

    def enter_email(self, email: str) -> None:
        self.fill(self.EMAIL_INPUT, email)

    def enter_password(self, password: str) -> None:
        self.fill(self.PASSWORD_INPUT, password)

    def click_login(self) -> None:
        self.click(self.LOGIN_BUTTON)

    def login(self, email: str, password: str) -> None:
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    # -------------------------
    # Assertions
    # -------------------------

    def assert_login_successful(self) -> None:
        self.expect_visible(self.SUCCESS_MESSAGE)

    def assert_login_failed(self) -> None:
        self.expect_visible(self.ERROR_MESSAGE)
    
    def assert_login_page(self) -> None:
        self.assert_heading(self.PAGE_HEADER)
