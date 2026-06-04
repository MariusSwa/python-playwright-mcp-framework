from pages.login_page import LoginPage
from core.config import BASE_URL


def test_user_can_login(page):
    login_page = LoginPage(page)

    login_page.open(BASE_URL)
    login_page.login("test@test.com", "Password123")
    login_page.assert_login_successful()


def test_wrong_password(page):
    login_page = LoginPage(page)

    login_page.open(BASE_URL)
    login_page.enter_email("test@123.com")
    login_page.enter_password("wrongPass")
    login_page.assert_login_successful()