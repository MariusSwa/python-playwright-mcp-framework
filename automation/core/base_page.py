from collections.abc import Callable
from typing import Any

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Locator, Page, expect

from core.locator_healer import LocatorHealer

LocatorConfig = dict[str, Any]


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def resolve_locator(self, locator: LocatorConfig) -> Locator:
        parent = locator.get("parent")
        if parent:
            return self._resolve_from(self.resolve_locator(parent), locator)
        return self._resolve_from(self.page, locator)

    def _resolve_from(self, target: Page | Locator, locator: LocatorConfig) -> Locator:
        locator_type = locator.get("type")

        if locator_type == "role":
            return target.get_by_role(
                locator["role"],
                name=locator["name"],
                exact=locator.get("exact", False),
            )

        if locator_type == "label":
            return target.get_by_label(locator["value"])

        if locator_type == "placeholder":
            return target.get_by_placeholder(locator["value"])

        if locator_type == "text":
            return target.get_by_text(locator["value"])

        if locator_type == "test_id":
            return target.get_by_test_id(locator["value"])

        if locator_type == "css":
            return target.locator(locator["value"])

        raise ValueError(f"Unknown locator type: {locator_type}")

    def goto(self, url: str) -> None:
        self.page.goto(url)

    def click(self, locator: LocatorConfig) -> None:
        self._run_with_locator_repair(locator, "click", lambda item: item.click())

    def fill(self, locator: LocatorConfig, value: str) -> None:
        self._run_with_locator_repair(locator, "fill", lambda item: item.fill(value))

    def check(self, locator: LocatorConfig) -> None:
        self._run_with_locator_repair(locator, "check", lambda item: item.check())

    def select_option(self, locator: LocatorConfig, value: str) -> None:
        self._run_with_locator_repair(
            locator,
            "select_option",
            lambda item: item.select_option(value),
        )

    def expect_visible(self, locator: LocatorConfig) -> None:
        self._run_with_locator_repair(
            locator,
            "expect_visible",
            lambda item: expect(item).to_be_visible(),
        )

    def expect_text(self, locator: LocatorConfig, text: str) -> None:
        self._run_with_locator_repair(
            locator,
            "expect_text",
            lambda item: expect(item).to_have_text(text),
        )

    def assert_heading(self, heading_text: str) -> None:
        heading = {
            "type": "role",
            "role": "heading",
            "name": heading_text,
        }
        self.expect_visible(heading)

    def assert_page_loaded(self) -> None:
        raise NotImplementedError("Page objects must implement assert_page_loaded().")

    def _run_with_locator_repair(
        self,
        locator: LocatorConfig,
        action: str,
        operation: Callable[[Locator], object],
    ) -> None:
        try:
            operation(self.resolve_locator(locator))
        except (AssertionError, PlaywrightError) as error:
            repaired_locator = LocatorHealer(self).repair_locator(
                locator=locator,
                action=action,
                error=error,
            )
            if repaired_locator is None:
                raise

            operation(self.resolve_locator(repaired_locator))
