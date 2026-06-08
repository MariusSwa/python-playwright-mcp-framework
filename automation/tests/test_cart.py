from components.navbar import Navbar
from core.config import BASE_URL, TEST_EMAIL, TEST_PASSWORD
from core.test_steps import step
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


def test_empty_cart_message_displayed(page):
    login_page = LoginPage(page)
    navbar = Navbar(page)
    cart_page = CartPage(page)

    with step("Login with valid credentials"):
        login_page.open(BASE_URL)
        login_page.login(TEST_EMAIL, TEST_PASSWORD)

    with step("Open cart page"):
        navbar.go_to_cart()
        cart_page.assert_page_loaded()
        cart_page.assert_cart_is_empty()


def test_remove_item_from_cart(page):
    login_page = LoginPage(page)
    navbar = Navbar(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)

    with step("Login with valid credentials"):
        login_page.open(BASE_URL)
        login_page.login(TEST_EMAIL, TEST_PASSWORD)

    with step("Add Mechanical Keyboard to cart"):
        navbar.go_to_products()
        products_page.assert_page_loaded()
        products_page.add_product_to_cart("Mechanical Keyboard")
        products_page.assert_product_added("Mechanical Keyboard")

    with step("Open cart page"):
        navbar.go_to_cart()
        cart_page.assert_page_loaded()
        cart_page.assert_product_is_displayed("Mechanical Keyboard")

    with step("Remove item from cart"):
        cart_page.remove_product("Mechanical Keyboard")
        cart_page.assert_cart_is_empty()
