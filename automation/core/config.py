import os
from pathlib import Path
from typing import cast

from dotenv import load_dotenv

ENV_FILE = Path(__file__).resolve().parents[2] / ".env.local"
load_dotenv(dotenv_path=ENV_FILE)

APP_ENV: str = os.getenv("APP_ENV", "local")
BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")
BROWSER: str = os.getenv("BROWSER", "chromium")
HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"

LOCATOR_REPAIR_MODE: str = os.getenv("LOCATOR_REPAIR_MODE", "off").lower()
LOCATOR_REPAIR_MIN_CONFIDENCE: float = float(
    os.getenv("LOCATOR_REPAIR_MIN_CONFIDENCE", "0.95")
)
LOCATOR_REPAIR_MAX_REPAIRS_PER_TEST: int = int(
    os.getenv("LOCATOR_REPAIR_MAX_REPAIRS_PER_TEST", "1")
)
LOCATOR_REPAIR_MAX_ATTEMPTS_PER_LOCATOR: int = int(
    os.getenv("LOCATOR_REPAIR_MAX_ATTEMPTS_PER_LOCATOR", "1")
)
LOCATOR_REPAIR_MAX_MCP_CALLS_PER_TEST: int = int(
    os.getenv("LOCATOR_REPAIR_MAX_MCP_CALLS_PER_TEST", "2")
)
LOCATOR_REPAIR_HISTORY_FILE: Path = (
    Path(__file__).resolve().parents[1] / "healing" / "history.json"
)
CI: bool = os.getenv("CI", "false").lower() == "true"

TEST_EMAIL = cast(str, os.getenv("TEST_EMAIL"))
TEST_PASSWORD = cast(str, os.getenv("TEST_PASSWORD"))

if not TEST_EMAIL or not TEST_PASSWORD:
    raise RuntimeError(
        f"TEST_EMAIL and TEST_PASSWORD must be set in {ENV_FILE}"
    )
