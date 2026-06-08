
from components.navbar import Navbar
from core.config import (
    BASE_URL,
    TEST_EMAIL,
    TEST_PASSWORD,
)
from core.test_steps import step
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


def test_dashboard_loads_after_login(page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    with step("Open login page"):
        login_page.open(BASE_URL)

    with step("Login with valid credentials"):
        login_page.login(TEST_EMAIL, TEST_PASSWORD)

    with step("Verify dashboard is displayed"):
        dashboard_page.assert_page_loaded()


def test_user_can_logout(page):
    login_page = LoginPage(page)
    navbar = Navbar(page)

    with step("Open login page"):
        login_page.open(BASE_URL)

    with step("Login with valid credentials"):
        login_page.login(TEST_EMAIL, TEST_PASSWORD)

    with step("Logout"):
        navbar.logout()

    with step("Verify login page is displayed"):
        login_page.assert_login_page()
