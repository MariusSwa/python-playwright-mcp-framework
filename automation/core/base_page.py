from playwright.sync_api import Page, expect


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def resolve_locator(self, locator: dict):
        locator_type = locator.get("type")

        if locator_type == "role":
            return self.page.get_by_role(
                locator["role"],
                name=locator["name"]
            )

        if locator_type == "label":
            return self.page.get_by_label(locator["value"])

        if locator_type == "placeholder":
            return self.page.get_by_placeholder(locator["value"])

        if locator_type == "text":
            return self.page.get_by_text(locator["value"])

        if locator_type == "test_id":
            return self.page.get_by_test_id(locator["value"])

        if locator_type == "css":
            return self.page.locator(locator["value"])

        raise ValueError(f"Unknown locator type: {locator_type}")

    def goto(self, url: str):
        self.page.goto(url)

    def click(self, locator: dict):
        self.resolve_locator(locator).click()

    def fill(self, locator: dict, value: str):
        self.resolve_locator(locator).fill(value)

    def expect_visible(self, locator: dict):
        expect(self.resolve_locator(locator)).to_be_visible()