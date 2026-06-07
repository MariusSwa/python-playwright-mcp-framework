
from core.config import (
    BASE_URL,
    TEST_EMAIL,
    TEST_PASSWORD,
)
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


def test_user_can_logout(page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    login_page.open(BASE_URL)

    print(f"EMAIL: {TEST_EMAIL}")
    print(f"PASSWORD: {TEST_PASSWORD}")

    login_page.login(TEST_EMAIL, TEST_PASSWORD)

    dashboard_page.assert_dashboard_loaded()

    dashboard_page.logout()

    dashboard_page.assert_login_page_loaded()