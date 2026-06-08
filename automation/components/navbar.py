from playwright.sync_api import Page

from core.base_page import BasePage


class Navbar(BasePage):
    DASHBOARD_LINK = {
        "type": "role",
        "role": "link",
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

    def __init__(self, page: Page):
        super().__init__(page)

    def go_to_dashboard(self):
        self.click(self.DASHBOARD_LINK)

    def go_to_products(self):
        self.click(self.PRODUCTS_LINK)

    def go_to_cart(self):
        self.click(self.CART_LINK)

    def go_to_profile(self):
        self.click(self.PROFILE_LINK)

    def logout(self):
        self.click(self.LOGOUT_BUTTON)