from playwright.sync_api import Page

from core.base_page import BasePage


class DashboardPage(BasePage):

    # -------------------------
    # Page setup
    # -------------------------

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self, base_url: str) -> None:
        self.goto(f"{base_url.rstrip('/')}/dashboard.html")

    PAGE_HEADER = "Dashboard"

    # Locators
    VIEW_PRODUCTS_BUTTON = {
        "type": "role",
        "role": "link",
        "name": "View Products",
    }

    VIEW_CART_BUTTON = {
        "type": "role",
        "role": "link",
        "name": "View Cart",
    }

    VIEW_PROFILE_BUTTON = {
        "type": "role",
        "role": "link",
        "name": "View Profile",
    }
   

    # Actions

    def open_products(self) -> None:
        self.click(self.VIEW_PRODUCTS_BUTTON)

    def open_cart(self) -> None:
        self.click(self.VIEW_CART_BUTTON)

    def open_profile(self) -> None:
        self.click(self.VIEW_PROFILE_BUTTON)

    # Assertions

    def assert_page_loaded(self) -> None:
        self.assert_heading(self.PAGE_HEADER)
