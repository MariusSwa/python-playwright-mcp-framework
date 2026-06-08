from playwright.sync_api import Page

from core.base_page import BasePage


class Navbar(BasePage):
    DASHBOARD_LINK = {
        "type": "role",
        "role": "link",
        "name": "Dashboard",
        "exact": True,
    }

    PRODUCTS_LINK = {
        "type": "role",
        "role": "link",
        "name": "Products",
        "exact": True,
    }

    CART_LINK = {
        "type": "role",
        "role": "link",
        "name": "Cart",
        "exact": True,
    }

    PROFILE_LINK = {
        "type": "role",
        "role": "link",
        "name": "Profile",
        "exact": True,
    }

    LOGOUT_BUTTON = {
        "type": "role",
        "role": "button",
        "name": "Logout",
        "exact": True,
    }

    def __init__(self, page: Page):
        super().__init__(page)

    def go_to_dashboard(self) -> None:
        self.click(self.DASHBOARD_LINK)

    def go_to_products(self) -> None:
        self.click(self.PRODUCTS_LINK)

    def go_to_cart(self) -> None:
        self.click(self.CART_LINK)

    def go_to_profile(self) -> None:
        self.click(self.PROFILE_LINK)

    def logout(self) -> None:
        self.click(self.LOGOUT_BUTTON)
