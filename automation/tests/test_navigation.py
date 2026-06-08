from components.navbar import Navbar
from core.config import BASE_URL, TEST_EMAIL, TEST_PASSWORD
from core.test_steps import step
from pages.cart_page import CartPage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.profile_page import ProfilePage


def test_navigation_links_work(page):
    login_page = LoginPage(page)
    navbar = Navbar(page)
    dashboard_page = DashboardPage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    profile_page = ProfilePage(page)

    with step("Open login page"):
        login_page.open(BASE_URL)

    with step("Login with valid credentials"):
        login_page.login(TEST_EMAIL, TEST_PASSWORD)

    with step("Navigate to dashboard page"):
        navbar.go_to_dashboard()
        dashboard_page.assert_page_loaded()

    with step("Navigate to products page"):
        navbar.go_to_products()
        products_page.assert_page_loaded()

    with step("Navigate to cart page"):
        navbar.go_to_cart()
        cart_page.assert_page_loaded()

    with step("Navigate to profile page"):
        navbar.go_to_profile()
        profile_page.assert_page_loaded()
