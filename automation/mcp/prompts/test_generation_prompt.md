# AI Test Generation Prompt

## Purpose

You are assisting with the development of a Python Playwright automation framework.

This framework is intended to become:

- A portfolio-quality Playwright framework
- A reusable automation template
- A future MCP-enabled framework
- A future AI-assisted test generation framework
- A future self-healing locator framework

Generated code must be maintainable, readable, beginner-friendly, and ready for future AI and MCP integration.

## Technology Stack

- Python 3.12+
- Playwright Python
- Pytest
- Ruff
- Mypy
- GitHub Actions
- Docker, future
- MCP, future

## Framework Design Rules

Every page object must use the Page Object Model and include:

- Locators
- Actions
- Assertions

Example:

```python
class LoginPage(BasePage):
    LOGIN_BUTTON = {
        "type": "role",
        "role": "button",
        "name": "Login",
    }

    def login(self, email: str, password: str) -> None:
        ...

    def assert_login_failed(self) -> None:
        ...
```

Shared UI elements must be implemented as components. Do not duplicate navbar locators in page objects. Examples include `Navbar`, `Toast`, `Modal`, `ProductCard`, and `Footer`.

## Preferred Locator Strategy

Always prefer Playwright recommended locators in this order:

1. `role`
2. `label`
3. `placeholder`
4. `text`
5. `test_id`
6. `css`, only when required

Avoid XPath, complex CSS selectors, and fragile locators.

Good locator examples:

```python
{"type": "role", "role": "button", "name": "Login"}
{"type": "label", "value": "Email"}
{"type": "test_id", "value": "login-message"}
```

## BasePage Rules

All interactions must flow through `BasePage` methods:

```python
self.click(...)
self.fill(...)
self.check(...)
self.select_option(...)
self.expect_visible(...)
self.assert_heading(...)
self.assert_page_loaded(...)
```

Do not call `page.get_by_role(...)`, `page.get_by_label(...)`, or `page.locator(...)` directly inside tests. Avoid direct Playwright calls inside page objects whenever practical.

## Environment Configuration

Local configuration is loaded from `.env.local`.

CI configuration is loaded from GitHub Actions secrets.

Use:

```python
from core.config import BASE_URL, TEST_EMAIL, TEST_PASSWORD
```

Do not hardcode credentials inside tests.

## Test Step Rules

Tests must use readable, business-level steps.
Where it remains clear, group closely related actions and assertions inside one business-level step. For example, opening a page and verifying it loaded can usually share one step.

Use:

```python
from core.test_steps import step
```

Example:

```python
with step("Open login page"):
    login_page.open(BASE_URL)

with step("Login with valid credentials"):
    login_page.login(TEST_EMAIL, TEST_PASSWORD)

with step("Verify dashboard is displayed"):
    dashboard_page.assert_page_loaded()
```

Good step names:

- Open login page
- Login with valid credentials
- Navigate to products page
- Add Wireless Mouse to cart
- Verify product added message is displayed
- Open cart page
- Remove item from cart
- Verify cart is empty

Avoid low-level step names such as `Click button`, `Fill field`, `Assert text`, and `Use locator`.

## Code Quality Requirements

Generated code must pass:

```bash
ruff check .
mypy .
pytest
```

Generated code must be readable, typed where practical, maintainable, consistent, and avoid unnecessary abstractions.

## MCP-Ready Rules

Do not implement MCP unless explicitly requested. Keep the framework MCP-ready.

Locators must remain visible and structured so future MCP healing can inspect locator metadata.

Good:

```python
LOGIN_BUTTON = {
    "type": "role",
    "role": "button",
    "name": "Login",
}
```

Bad:

```python
page.get_by_role("button", name="Login")
```

Future self-healing flow:

```text
Locator fails
Framework captures page context
MCP analyzes page
Replacement locator suggested
Retry action
Store healing history
```

All interactions must be capable of passing through `resolve_locator()` inside `BasePage`.

Future AI test generation flow:

```text
Page
DOM analysis
LLM
Test suggestion
Developer review
Framework integration
```

Generated tests should be readable, independent, reusable, and business-focused.

## Demo Application

Pages:

- Login
- Dashboard
- Products
- Cart
- Profile

Navbar:

- Dashboard
- Products
- Cart
- Profile
- Logout

Products:

- Wireless Mouse
- Mechanical Keyboard
- USB-C Hub
- Laptop Stand

## Desired Test Coverage

Login:

- `test_user_can_login`
- `test_invalid_login_shows_error`

Dashboard:

- `test_dashboard_loads_after_login`
- `test_user_can_logout`

Products:

- `test_products_page_loads`
- `test_add_product_to_cart`

Cart:

- `test_empty_cart_message_displayed`
- `test_remove_item_from_cart`

Profile:

- `test_profile_page_loads`
- `test_user_can_update_profile`

Navigation:

- `test_navigation_links_work`

## Acceptance Criteria

Generated code must:

- Follow the framework structure
- Use page objects
- Use components
- Use preferred locators
- Use test steps
- Support Ruff
- Support Mypy
- Support Pytest
- Support future MCP integration
- Remain beginner-friendly

When generating code, always follow these rules unless explicitly instructed otherwise.
