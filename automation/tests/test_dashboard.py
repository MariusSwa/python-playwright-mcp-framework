
from components.navbar import Navbar
from core.config import (
    BASE_URL,
    TEST_EMAIL,
    TEST_PASSWORD,
)
from core.test_steps import step
from pages.login_page import LoginPage


def test_logout(page):
    login_page = LoginPage(page)
    navbar_comp = Navbar(page)

    with step("Open Web Appliaction"):
        login_page = LoginPage(page)
        login_page.open(BASE_URL)

    with step("Login"):
        login_page.login(TEST_EMAIL, TEST_PASSWORD)
        login_page.assert_login_successful()
    
    with step("Logout"):
       navbar_comp.logout()
       login_page.assert_login_page()