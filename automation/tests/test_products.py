from components.navbar import Navbar
from core.config import BASE_URL, TEST_EMAIL, TEST_PASSWORD
from core.test_steps import step
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


def test_products_page_loads(page):
    login_page = LoginPage(page)
    navbar = Navbar(page)
    products_page = ProductsPage(page)

    with step("Login with valid credentials"):
        login_page.open(BASE_URL)
        login_page.login(TEST_EMAIL, TEST_PASSWORD)

    with step("Open products page"):
        navbar.go_to_products()
        products_page.assert_page_loaded()
        products_page.assert_product_is_displayed("Mechanical Keyboard")


def test_add_product_to_cart(page):
    login_page = LoginPage(page)
    navbar = Navbar(page)
    products_page = ProductsPage(page)

    with step("Login with valid credentials"):
        login_page.open(BASE_URL)
        login_page.login(TEST_EMAIL, TEST_PASSWORD)

    with step("Open products page"):
        navbar.go_to_products()
        products_page.assert_page_loaded()

    with step("Add Wireless Mouse to cart"):
        products_page.add_product_to_cart("Wireless Mouse")
        products_page.assert_product_added("Wireless Mouse")
