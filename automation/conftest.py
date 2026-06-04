import os
import pytest
from datetime import datetime


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        page = item.funcargs.get("page")

        if page:

            os.makedirs("screenshots", exist_ok=True)

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            screenshot_path = (
                f"screenshots/"
                f"{item.name}_{timestamp}.png"
            )

            page.screenshot(
                path=screenshot_path,
                full_page=True
            )

            print(
                f"\nScreenshot saved: "
                f"{screenshot_path}"
            )