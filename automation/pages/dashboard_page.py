from playwright.sync_api import Page

from core.base_page import BasePage




class DashboardPage(BasePage):

    # -------------------------
    # Page setup
    # -------------------------

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self, base_url: str):
        self.goto(base_url)


    # Locators
    DASHBOARD_HEADING = {
        "type": "role",
        "role": "heading",
        "name": "Dashboard",
    }

    PRODUCTS_LINK = {
        "type": "role",
        "role": "link",
        "name": "Products",
    }

    CART_LINK = {
        "type": "role",
        "role": "link",
        "name": "Cart",
    }

    PROFILE_LINK = {
        "type": "role",
        "role": "link",
        "name": "Profile",
    }

    LOGOUT_BUTTON = {
        "type": "role",
        "role": "button",
        "name": "Logout",
    }

    LOGIN_HEADING = {
        "type": "role",
        "role": "heading",
        "name": "Login",
    }

    # Actions
    def click_products(self):
        self.click(self.PRODUCTS_LINK)

    def click_cart(self):
        self.click(self.CART_LINK)

    def click_profile(self):
        self.click(self.PROFILE_LINK)

    def logout(self):
        self.click(self.LOGOUT_BUTTON)

    # Assertions
    def assert_dashboard_loaded(self):
        self.expect_visible(self.DASHBOARD_HEADING)

    def assert_login_page_loaded(self):
        self.expect_visible(self.LOGIN_HEADING)