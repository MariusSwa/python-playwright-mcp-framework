import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env.local")

APP_ENV = os.getenv("APP_ENV", "local")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
BROWSER = os.getenv("BROWSER", "chromium")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"