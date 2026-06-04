from playwright.sync_api import Page

from core.base_page import BasePage


class LoginPage(BasePage):

    # -------------------------
    # Page setup
    # -------------------------

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self, base_url: str):
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
        "role": "check",
        "name": "rememberMe"
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

    # -------------------------
    # Actions
    # -------------------------

    def enter_email(self, email: str):
        self.fill(self.EMAIL_INPUT, email)

    def enter_password(self, password: str):
        self.fill(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def login(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    # -------------------------
    # Assertions
    # -------------------------

    def assert_login_successful(self):
        self.expect_visible(self.SUCCESS_MESSAGE)