
from core.config import (
    BASE_URL,
    TEST_EMAIL,
    TEST_PASSWORD,
)
from core.test_steps import step
from pages.login_page import LoginPage


def test_user_can_login(page):
    with step("Open Web Appliaction"):
        login_page = LoginPage(page)
        login_page.open(BASE_URL)

    with step("Login"):
        login_page.login(TEST_EMAIL, TEST_PASSWORD)
        login_page.assert_login_successful()

# @pytest.mark.xfail(reason="Intentional failure to verify screenshot reporting")
def test_wrong_password(page):

    with step("Open Web Appliaction"):
        login_page = LoginPage(page)
        login_page.open(BASE_URL)

    with step("Incorrect login"):
        login_page.enter_email(TEST_EMAIL)
        login_page.enter_password("wrongPass")
        login_page.assert_login_failed()