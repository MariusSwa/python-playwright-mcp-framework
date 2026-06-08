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
    def assert_dashboard_loaded(self):
        self.assert_heading(self.PAGE_HEADER)