import base64
from datetime import datetime
from pathlib import Path

import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page:
            screenshot_dir = Path("reports") / "screenshots"
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f"{item.name}_{timestamp}.png"
            screenshot_path = screenshot_dir / screenshot_filename
            report_screenshot_path = f"screenshots/{screenshot_filename}"

            screenshot_bytes = page.screenshot(
                path=str(screenshot_path),
                full_page=True,
            )
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")

            print(f"\nScreenshot saved: {screenshot_path}")

            pytest_html = item.config.pluginmanager.getplugin("html")

            if pytest_html:
                extras = getattr(report, "extras", [])
                if item.config.getoption("self_contained_html"):
                    extras.append(
                        pytest_html.extras.png(
                            screenshot_base64,
                            name=report_screenshot_path,
                        )
                    )
                else:
                    extras.append(pytest_html.extras.image(report_screenshot_path))
                report.extras = extras
