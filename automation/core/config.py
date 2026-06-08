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

TEST_EMAIL = cast(str, os.getenv("TEST_EMAIL"))
TEST_PASSWORD = cast(str, os.getenv("TEST_PASSWORD"))

if not TEST_EMAIL or not TEST_PASSWORD:
    raise RuntimeError(
        f"TEST_EMAIL and TEST_PASSWORD must be set in {ENV_FILE}"
    )
