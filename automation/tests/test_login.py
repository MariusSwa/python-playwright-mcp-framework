
from core.config import (
    BASE_URL,
    TEST_EMAIL,
    TEST_PASSWORD,
)
from core.test_steps import step
from pages.login_page import LoginPage


def test_user_can_login(page):
    with step("Open login page"):
        login_page = LoginPage(page)
        login_page.open(BASE_URL)

    with step("Login with valid credentials"):
        login_page.login(TEST_EMAIL, TEST_PASSWORD)

    with step("Verify login success message is displayed"):
        login_page.assert_login_successful()


def test_invalid_login_shows_error(page):
    with step("Open login page"):
        login_page = LoginPage(page)
        login_page.open(BASE_URL)

    with step("Login with invalid credentials"):
        login_page.login(TEST_EMAIL, "wrongPass")

    with step("Verify login error message is displayed"):
        login_page.assert_login_failed()
