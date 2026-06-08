from playwright.sync_api import Page

from core.base_page import BasePage


class ProfilePage(BasePage):
    PAGE_HEADER = "Profile"

    FIRST_NAME_INPUT = {
        "type": "label",
        "value": "First Name",
    }

    LAST_NAME_INPUT = {
        "type": "label",
        "value": "Last Name",
    }

    EMAIL_INPUT = {
        "type": "label",
        "value": "Email",
    }

    SAVE_PROFILE_BUTTON = {
        "type": "role",
        "role": "button",
        "name": "Save Profile",
    }

    PROFILE_MESSAGE = {
        "type": "test_id",
        "value": "profile-message",
    }

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self, base_url: str) -> None:
        self.goto(f"{base_url.rstrip('/')}/profile.html")

    def update_profile(self, first_name: str, last_name: str, email: str) -> None:
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.EMAIL_INPUT, email)
        self.click(self.SAVE_PROFILE_BUTTON)

    def assert_page_loaded(self) -> None:
        self.assert_heading(self.PAGE_HEADER)

    def assert_profile_saved(self) -> None:
        self.expect_text(self.PROFILE_MESSAGE, "Profile saved successfully.")
