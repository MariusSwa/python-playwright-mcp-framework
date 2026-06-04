from playwright.sync_api import Page


class LocatorHealer:
    def __init__(self, page: Page):
        self.page = page

    def get_page_snapshot(self) -> str:
        return self.page.locator("body").inner_text(timeout=3000)

    def suggest_new_locator(self, old_locator: str, intent: str) -> list[str]:
        snapshot = self.get_page_snapshot()

        # Temporary placeholder.
        # Later this will call the MCP self-healing server.
        suggestions = []

        if "Login" in snapshot:
            suggestions.append("button:has-text('Login')")

        return suggestions