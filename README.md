# Python Playwright MCP Automation Framework

[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/playwright-python-2EAD33.svg)](https://playwright.dev/python/)
[![Pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC.svg)](https://docs.pytest.org/)
[![Ruff](https://img.shields.io/badge/linting-ruff-D7FF64.svg)](https://docs.astral.sh/ruff/)
[![Mypy](https://img.shields.io/badge/types-mypy-blue.svg)](https://mypy-lang.org/)
[![MCP](https://img.shields.io/badge/MCP-ready-purple.svg)](https://modelcontextprotocol.io/)
[![Code Quality](https://github.com/MariusSwa/python-playwright-mcp-framework/actions/workflows/code-quality.yml/badge.svg)](https://github.com/MariusSwa/python-playwright-mcp-framework/actions/workflows/code-quality.yml)
[![Run Automation Tests](https://github.com/MariusSwa/python-playwright-mcp-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/MariusSwa/python-playwright-mcp-framework/actions/workflows/tests.yml)

A Python Playwright automation framework built around maintainable page objects, preferred Playwright locators, readable pytest steps, HTML reporting, GitHub Actions, and local MCP-ready locator repair.

The demo application is a static ecommerce-style site with Login, Dashboard, Products, Cart, and Profile pages.

## Features

- Python 3.12+ automation framework
- Playwright Python browser automation
- Pytest test execution
- Page Object Model
- Reusable components, such as `Navbar`
- Structured locator dictionaries for future MCP/AI inspection
- Preferred Playwright locators
- Business-readable test steps
- HTML reports and failure screenshots
- Ruff linting
- Mypy static analysis
- GitHub Actions for code quality and test execution
- Local configurable locator repair with audit history

## Project Structure

```text
source/
|-- app/                         # Static demo web application
|   |-- index.html
|   |-- dashboard.html
|   |-- products.html
|   |-- cart.html
|   |-- profile.html
|   `-- assets/
|
|-- automation/                  # Playwright automation framework
|   |-- components/
|   |   `-- navbar.py
|   |-- core/
|   |   |-- base_page.py
|   |   |-- config.py
|   |   |-- locator_healer.py
|   |   `-- test_steps.py
|   |-- healing/
|   |   `-- history.json
|   |-- mcp/
|   |   |-- client.py
|   |   |-- prompts/
|   |   `-- servers/
|   |       `-- self_healing_server.py
|   |-- pages/
|   |   |-- login_page.py
|   |   |-- dashboard_page.py
|   |   |-- products_page.py
|   |   |-- cart_page.py
|   |   `-- profile_page.py
|   |-- reports/
|   |-- tests/
|   |   |-- test_login.py
|   |   |-- test_dashboard.py
|   |   |-- test_products.py
|   |   |-- test_cart.py
|   |   |-- test_profile.py
|   |   `-- test_navigation.py
|   |-- requirements.txt
|   |-- pytest.ini
|   |-- ruff.toml
|   `-- mypy.ini
|
|-- .github/
|   `-- workflows/
|       |-- code-quality.yml
|       `-- tests.yml
|
|-- docker/
|-- .env-example
|-- .env.local
`-- README.md
```

## Requirements

- Python 3.12+
- Git
- A terminal such as PowerShell, Bash, or VS Code terminal
- Optional: Docker Desktop for future container work

## Installation

Clone the repository:

```bash
git clone https://github.com/MariusSwa/python-playwright-mcp-framework.git
cd python-playwright-mcp-framework
```

Create and activate a virtual environment from the `automation` folder:

```bash
cd automation
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows command prompt:

```cmd
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install
```

## Environment Setup

Create a local environment file from the project root:

```bash
cp .env-example .env.local
```

On Windows PowerShell:

```powershell
Copy-Item .env-example .env.local
```

Required local values:

```env
APP_ENV=local
BASE_URL=http://localhost:8000
BROWSER=chromium
HEADLESS=true

TEST_EMAIL=test@example.com
TEST_PASSWORD=Password123
```

The demo application currently accepts:

```text
Email: test@example.com
Password: Password123
```

## Run the Demo Site

Open a terminal from the project root:

```bash
cd app
python -m http.server 8000
```

Open the app in a browser:

```text
http://localhost:8000
```

Keep this terminal running while executing tests.

## Run Tests

Open a second terminal:

```bash
cd automation
```

Activate the virtual environment, then run:

```bash
pytest
```

Run one test file:

```bash
pytest tests/test_login.py
```

Run one test:

```bash
pytest tests/test_login.py::test_user_can_login
```

Reports are generated at:

```text
automation/reports/report.html
```

Failure screenshots are saved in:

```text
automation/reports/screenshots/
```

## Code Quality

Run Ruff:

```bash
ruff check .
```

Auto-fix Ruff issues:

```bash
ruff check . --fix
```

Format code:

```bash
ruff format .
```

Run Mypy:

```bash
mypy .
```

Recommended local check before pushing:

```bash
ruff check .
mypy .
pytest
```

## GitHub Actions

This repository includes two workflows.

### Code Quality

File:

```text
.github/workflows/code-quality.yml
```

Runs on pull requests to `main` and manual `workflow_dispatch`.

Checks:

- Install Python 3.12
- Install `automation/requirements.txt`
- Run `ruff check .`
- Run `mypy .`

### Run Automation Tests

File:

```text
.github/workflows/tests.yml
```

Runs on pull requests to `main` and manual `workflow_dispatch`.

Checks:

- Use the official Playwright Python container
- Install automation dependencies
- Install Playwright browsers
- Start the static demo site
- Run `pytest`
- Upload `automation/reports/` as an artifact

The test workflow expects these GitHub Actions secrets:

```text
TEST_EMAIL
TEST_PASSWORD
```

Locator repair is disabled in CI when `CI=true`.

## Framework Design

The framework uses the Page Object Model. Tests should describe user behavior, while page objects handle locators and browser interactions.

Each page object should contain:

- Locators
- Actions
- Assertions

Example:

```python
from playwright.sync_api import Page

from core.base_page import BasePage


class LoginPage(BasePage):
    PAGE_HEADER = "Login"

    # Locators
    EMAIL_INPUT = {
        "type": "label",
        "value": "Email",
    }

    PASSWORD_INPUT = {
        "type": "label",
        "value": "Password",
    }

    LOGIN_BUTTON = {
        "type": "role",
        "role": "button",
        "name": "Login",
        "exact": True,
    }

    ERROR_MESSAGE = {
        "type": "test_id",
        "value": "login-message",
    }

    def __init__(self, page: Page):
        super().__init__(page)

    # Actions
    def open(self, base_url: str) -> None:
        self.goto(base_url)

    def login(self, email: str, password: str) -> None:
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    # Assertions
    def assert_login_failed(self) -> None:
        self.expect_visible(self.ERROR_MESSAGE)
```

Tests should not call Playwright directly. Use page object methods instead.

Avoid this in tests:

```python
page.get_by_role("button", name="Login").click()
```

Prefer this:

```python
login_page.login(TEST_EMAIL, TEST_PASSWORD)
```

## Components

Shared UI should be modeled as components. The navbar is implemented in:

```text
automation/components/navbar.py
```

Example usage:

```python
from components.navbar import Navbar


navbar = Navbar(page)
navbar.go_to_products()
```

Use components when the same UI appears across multiple pages, such as:

- Navbar
- Toast
- Modal
- Product card
- Footer

## Preferred Locators

Use Playwright recommended locators in this order:

1. Role
2. Label
3. Placeholder
4. Text
5. Test ID
6. CSS fallback only when required

Avoid:

- XPath
- Complex CSS selectors
- Position-based locators
- Brittle DOM-depth selectors

### Role Locator

Use for buttons, links, headings, checkboxes, and other accessible elements.

```python
LOGIN_BUTTON = {
    "type": "role",
    "role": "button",
    "name": "Login",
    "exact": True,
}
```

`exact=True` means the accessible name must match exactly. For example, `Cart` will not also match `View Cart`.

### Label Locator

Use for inputs with labels.

```python
EMAIL_INPUT = {
    "type": "label",
    "value": "Email",
}
```

### Placeholder Locator

Use when a field has no useful label but has a stable placeholder.

```python
SEARCH_INPUT = {
    "type": "placeholder",
    "value": "Search products",
}
```

### Text Locator

Use for stable visible text.

```python
SUCCESS_MESSAGE = {
    "type": "text",
    "value": "Login successful",
}
```

### Test ID Locator

Use when the application exposes stable `data-testid` attributes.

```python
ERROR_MESSAGE = {
    "type": "test_id",
    "value": "login-message",
}
```

### Scoped Locators

Use `parent` when a locator should be resolved inside another element.

```python
PRODUCT_CARD = {
    "type": "test_id",
    "value": "product-wireless-mouse",
}

ADD_TO_CART_BUTTON = {
    "type": "role",
    "role": "button",
    "name": "Add to Cart",
    "exact": True,
    "parent": PRODUCT_CARD,
}
```

### CSS Fallback

Use CSS only when preferred locators are not practical.

```python
SUCCESS_TOAST = {
    "type": "css",
    "value": ".toast.success",
}
```

## BasePage Methods

All page object actions should flow through `BasePage`.

Available helpers include:

```python
self.goto(url)
self.click(locator)
self.fill(locator, value)
self.check(locator)
self.select_option(locator, value)
self.expect_visible(locator)
self.expect_text(locator, text)
self.assert_heading("Dashboard")
```

This keeps interactions centralized and allows locator repair to intercept failures.

## Writing Tests

Tests use business-readable steps from `core.test_steps`.

Example:

```python
from core.config import BASE_URL, TEST_EMAIL, TEST_PASSWORD
from core.test_steps import step
from pages.login_page import LoginPage


def test_user_can_login(page):
    login_page = LoginPage(page)

    with step("Open login page"):
        login_page.open(BASE_URL)

    with step("Login with valid credentials"):
        login_page.login(TEST_EMAIL, TEST_PASSWORD)

    with step("Verify login success message is displayed"):
        login_page.assert_login_successful()
```

Where it remains clear, group related actions and assertions in one business-level step:

```python
with step("Open products page"):
    navbar.go_to_products()
    products_page.assert_page_loaded()
    products_page.assert_product_is_displayed("Mechanical Keyboard")
```

Good step names:

- Open login page
- Login with valid credentials
- Open products page
- Add Wireless Mouse to cart
- Remove item from cart
- Verify cart is empty

Avoid low-level step names:

- Click button
- Fill field
- Assert text
- Use locator

## Adding a New Page Object

1. Create a file in `automation/pages/`, for example `orders_page.py`.
2. Create a class that inherits from `BasePage`.
3. Add structured locator dictionaries.
4. Add action methods for user behavior.
5. Add assertion methods for expected page state.
6. Write tests that use the page object.

Template:

```python
from playwright.sync_api import Page

from core.base_page import BasePage


class OrdersPage(BasePage):
    PAGE_HEADER = "Orders"

    CREATE_ORDER_BUTTON = {
        "type": "role",
        "role": "button",
        "name": "Create Order",
        "exact": True,
    }

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self, base_url: str) -> None:
        self.goto(f"{base_url.rstrip('/')}/orders.html")

    def create_order(self) -> None:
        self.click(self.CREATE_ORDER_BUTTON)

    def assert_page_loaded(self) -> None:
        self.assert_heading(self.PAGE_HEADER)
```

## Local Locator Repair

The framework currently has local MCP-ready locator repair. It does not call an external AI model yet.

Current flow:

```text
Locator action fails
BasePage catches the Playwright locator failure
LocatorHealer captures page context
Local self_healing_server.py suggests a structured replacement locator
Suggestion must meet the configured confidence threshold
Replacement must resolve to exactly one visible element
Interactive actions also require the element to be enabled
In repair mode, the page object locator is patched locally
The failed action is retried
Repair event is written to automation/healing/history.json
```

Current implementation:

- Local file: `automation/mcp/servers/self_healing_server.py`
- Orchestrator: `automation/core/locator_healer.py`
- Audit log: `automation/healing/history.json`

The current suggestion logic is deterministic and local. It is MCP-ready, but it is not yet connected to an external MCP host or paid LLM.

### Repair Settings

Configure repair in `.env.local`:

```env
LOCATOR_REPAIR_MODE=off
LOCATOR_REPAIR_MIN_CONFIDENCE=0.95
LOCATOR_REPAIR_MAX_REPAIRS_PER_TEST=1
LOCATOR_REPAIR_MAX_ATTEMPTS_PER_LOCATOR=1
LOCATOR_REPAIR_MAX_MCP_CALLS_PER_TEST=2
```

Modes:

```text
off      No repair.
dry_run  Suggest and log repairs, but do not patch code.
repair   Validate, patch the page object, and retry the failed action locally.
```

Cost and safety controls:

- `LOCATOR_REPAIR_MIN_CONFIDENCE`: minimum confidence needed before repair is accepted.
- `LOCATOR_REPAIR_MAX_REPAIRS_PER_TEST`: total accepted repairs allowed per test.
- `LOCATOR_REPAIR_MAX_ATTEMPTS_PER_LOCATOR`: how many times the same locator may be repaired in one test.
- `LOCATOR_REPAIR_MAX_MCP_CALLS_PER_TEST`: maximum suggestion calls allowed per test, including rejected suggestions.

Repair is blocked when:

- `LOCATOR_REPAIR_MODE=off`
- `CI=true`
- Confidence is below the threshold
- Per-test repair limit is reached
- Per-locator repair limit is reached
- MCP/suggestion call limit is reached
- The replacement locator does not resolve to exactly one valid element
- The locator is dynamic and cannot be safely patched as a static page-object locator

Run in dry-run mode:

```powershell
$env:LOCATOR_REPAIR_MODE = "dry_run"
pytest tests/test_login.py
```

Run in repair mode:

```powershell
$env:LOCATOR_REPAIR_MODE = "repair"
$env:LOCATOR_REPAIR_MIN_CONFIDENCE = "0.95"
pytest tests/test_login.py
```

Or set these values directly in `.env.local`.

## Current Test Coverage

- Login
- Dashboard
- Products
- Cart
- Profile
- Navigation

## Recommended Local Workflow

```bash
cd automation
ruff check .
mypy .
pytest
```

For day-to-day development, keep locator repair off unless you are intentionally testing or repairing broken locators.
