# Python Playwright MCP Automation Framework

A Python-based Playwright automation framework built for a third-year project and portfolio template.

The framework is designed to support:

* Playwright with Python
* Pytest test execution
* Page Object Model
* Preferred Playwright locators
* Screenshot reporting
* Ruff linting
* Mypy static analysis
* GitHub Actions
* Future MCP support for self-healing locators and AI test generation

---

# Project Structure

```text
source/
├── app/                         # Static demo web application
│   ├── index.html
│   ├── dashboard.html
│   ├── products.html
│   ├── cart.html
│   ├── profile.html
│   └── assets/
│
├── automation/                  # Playwright automation framework
│   ├── core/
│   │   ├── base_page.py
│   │   ├── config.py
│   │   └── locator_resolver.py
│   │
│   ├── pages/
│   │   └── login_page.py
│   │
│   ├── tests/
│   │   └── test_login.py
│   │
│   ├── mcp/                     # Future MCP server/client work
│   ├── reports/
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── ruff.toml
│   └── mypy.ini
│
├── .github/
│   └── workflows/
│       ├── code-quality.yml
│       └── tests.yml
│
└── README.md
```

---

# Requirements

Install these globally:

```bash
python --version
git --version
```

Recommended:

```text
Python 3.12+
Git
VS Code
Docker Desktop (optional for future use)
```

Playwright browsers are installed inside the Python virtual environment.

---

# Clone the Repository

```bash
git clone https://github.com/MariusSwa/python-playwright-mcp-framework.git
cd python-playwright-mcp-framework
```

---

# Create and Activate Virtual Environment

From the automation folder:

```bash
cd automation
python -m venv .venv
```

Activate on Windows PowerShell:

```bash
.venv\Scripts\activate
```

You should see:

```text
(.venv)
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install
```

---

# Run the Demo Site

Open a terminal from the project root:

```bash
cd app
python -m http.server 8000
```

Open the application:

```text
http://localhost:8000
```

Keep this terminal running while executing tests.

---

# Run Tests

Open a second terminal:

```bash
cd automation
.venv\Scripts\activate
pytest -s
```

Run a specific test file:

```bash
pytest tests/test_login.py -s
```

Reports are generated in:

```text
automation/reports/report.html
```

Failure screenshots are stored in:

```text
automation/reports/screenshots/
```

---

# Code Quality

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

Run all local checks:

```bash
ruff check .
mypy .
pytest
```

---

# Page Object Design

Each page object should be split into three sections:

```text
Locators
Actions
Assertions
```

Example:

```python
class LoginPage(BasePage):

    # Locators
    EMAIL_INPUT = {
        "type": "label",
        "value": "Email",
    }

    LOGIN_BUTTON = {
        "type": "role",
        "role": "button",
        "name": "Login",
    }

    # Actions
    def login(self, email: str, password: str):
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    # Assertions
    def assert_error_message_visible(self):
        self.expect_visible(self.ERROR_MESSAGE)
```

This keeps locator changes separate from test actions.

If a locator changes, it should only be updated once.

---

# Preferred Playwright Locators

This framework uses Playwright's preferred locators wherever possible.

Preferred order:

```text
1. get_by_role()
2. get_by_label()
3. get_by_placeholder()
4. get_by_text()
5. get_by_test_id()
6. CSS fallback only when needed
```

Avoid XPath unless absolutely necessary.

---

# Locator Examples

## Button

HTML:

```html
<button>Login</button>
```

Locator:

```python
LOGIN_BUTTON = {
    "type": "role",
    "role": "button",
    "name": "Login",
}
```

---

## Text Input with Label

HTML:

```html
<label for="email">Email</label>
<input id="email" type="email">
```

Locator:

```python
EMAIL_INPUT = {
    "type": "label",
    "value": "Email",
}
```

---

## Password Field

HTML:

```html
<label for="password">Password</label>
<input id="password" type="password">
```

Locator:

```python
PASSWORD_INPUT = {
    "type": "label",
    "value": "Password",
}
```

---

## Placeholder

HTML:

```html
<input placeholder="Search products">
```

Locator:

```python
SEARCH_INPUT = {
    "type": "placeholder",
    "value": "Search products",
}
```

---

## Link

HTML:

```html
<a href="products.html">Products</a>
```

Locator:

```python
PRODUCTS_LINK = {
    "type": "role",
    "role": "link",
    "name": "Products",
}
```

---

## Heading

HTML:

```html
<h1>Dashboard</h1>
```

Locator:

```python
DASHBOARD_HEADING = {
    "type": "role",
    "role": "heading",
    "name": "Dashboard",
}
```

---

## Visible Text

HTML:

```html
<p>Invalid email or password</p>
```

Locator:

```python
ERROR_MESSAGE = {
    "type": "text",
    "value": "Invalid email or password",
}
```

---

## Test ID

HTML:

```html
<button data-testid="add-to-cart-wireless-mouse">
  Add to Cart
</button>
```

Locator:

```python
ADD_TO_CART_BUTTON = {
    "type": "test_id",
    "value": "add-to-cart-wireless-mouse",
}
```

---

## CSS Fallback

Only use when preferred locators are not practical.

HTML:

```html
<div class="toast success">Saved successfully</div>
```

Locator:

```python
SUCCESS_TOAST = {
    "type": "css",
    "value": ".toast.success",
}
```

---

# Why Preferred Locators Matter

Preferred Playwright locators make tests more stable because they locate elements the way users interact with the page.

Better:

```python
page.get_by_role("button", name="Login")
```

Less ideal:

```python
page.locator("#login-btn")
```

If the button ID changes, the CSS locator breaks.

If the button text and role remain the same, the preferred locator still works.

This also helps future MCP self-healing because each locator contains useful metadata such as:

```text
role
name
label
text
intent
```

---

# GitHub Actions

This project includes two workflows:

```text
code-quality.yml
tests.yml
```

## Code Quality Workflow

Runs:

```text
Ruff
Mypy
```

## Test Workflow

Runs:

```text
Install dependencies
Install Playwright browsers
Start demo site
Run Pytest
Upload reports
```

---

# Future MCP Features

The framework is prepared for future MCP integration:

```text
MCP self-healing locators
AI-generated Playwright tests
DOM snapshot analysis
Locator history
Healing reports
```

Planned flow:

```text
Locator fails
↓
Framework captures page context
↓
MCP server analyzes DOM
↓
Suggested locator returned
↓
Test retries
↓
Healing result stored
```

---

# Recommended Local Workflow

```bash
cd automation
.venv\Scripts\activate

ruff check .
mypy .
pytest
```

Before pushing code:

```bash
git status
git add .
git commit -m "Your commit message"
git push
```

---

# Current Demo Login

Valid demo user:

```text
Email: test@example.com
Password: Password123
```
