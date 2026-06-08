from components.navbar import Navbar
from core.config import BASE_URL, TEST_EMAIL, TEST_PASSWORD
from core.test_steps import step
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage


def test_profile_page_loads(page):
    login_page = LoginPage(page)
    navbar = Navbar(page)
    profile_page = ProfilePage(page)

    with step("Open login page"):
        login_page.open(BASE_URL)

    with step("Login with valid credentials"):
        login_page.login(TEST_EMAIL, TEST_PASSWORD)

    with step("Open profile page"):
        navbar.go_to_profile()

    with step("Verify profile page is displayed"):
        profile_page.assert_page_loaded()


def test_user_can_update_profile(page):
    login_page = LoginPage(page)
    navbar = Navbar(page)
    profile_page = ProfilePage(page)

    with step("Open login page"):
        login_page.open(BASE_URL)

    with step("Login with valid credentials"):
        login_page.login(TEST_EMAIL, TEST_PASSWORD)

    with step("Open profile page"):
        navbar.go_to_profile()

    with step("Update profile details"):
        profile_page.update_profile("Taylor", "Tester", TEST_EMAIL)

    with step("Verify profile saved message is displayed"):
        profile_page.assert_profile_saved()
