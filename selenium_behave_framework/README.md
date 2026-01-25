# Selenium Behave POM Framework

A comprehensive test automation framework using **Selenium WebDriver**, **Behave (BDD)**, **Page Object Model (POM)**, and **Keyword-Driven Testing** with Python.

## Features

- **Page Object Model (POM)** - Clean separation of test logic and page elements
- **Behave BDD Framework** - Gherkin syntax for human-readable test scenarios
- **Keyword-Driven Testing** - Excel-based test execution for non-technical users
- **Multi-Browser Support** - Chrome, Firefox, Edge with WebDriver Manager
- **Comprehensive Reporting** - HTML reports with screenshots
- **Configurable Execution** - Environment-based configuration
- **40+ Keywords** - Extensive keyword library for automation
- **Parallel Ready** - Support for parallel test execution

## Project Structure

```
selenium_behave_framework/
├── config/                     # Configuration management
│   ├── config.py              # Framework configuration
│   └── environments.py        # Environment-specific settings
├── pages/                      # Page Object Model
│   ├── base_page.py           # Base page with common methods
│   ├── login_page.py          # Login page object
│   ├── inventory_page.py      # Inventory/Products page object
│   ├── cart_page.py           # Shopping cart page object
│   └── checkout_page.py       # Checkout pages objects
├── features/                   # Behave BDD features
│   ├── login.feature          # Login test scenarios
│   ├── inventory.feature      # Inventory test scenarios
│   ├── cart.feature           # Cart test scenarios
│   ├── checkout.feature       # Checkout test scenarios
│   ├── e2e.feature            # End-to-end scenarios
│   ├── environment.py         # Behave hooks
│   └── steps/                 # Step definitions
│       ├── login_steps.py
│       ├── inventory_steps.py
│       ├── cart_steps.py
│       └── checkout_steps.py
├── keywords/                   # Keyword-driven engine
│   ├── keyword_engine.py      # 40+ automation keywords
│   └── keyword_executor.py    # Test execution manager
├── utils/                      # Utilities
│   ├── driver_factory.py      # WebDriver factory
│   ├── wait_helper.py         # Wait conditions
│   ├── excel_reader.py        # Excel data reader
│   ├── logger.py              # Logging utility
│   └── report_generator.py    # HTML report generator
├── test_data/                  # Test data files
├── reports/                    # Generated reports
├── screenshots/                # Test screenshots
├── logs/                       # Execution logs
├── run_tests.py               # Main test runner
├── create_sample_testdata.py  # Sample data generator
├── behave.ini                 # Behave configuration
├── requirements.txt           # Python dependencies
└── .env.example               # Environment template
```

## Installation

```bash
# Clone or navigate to the project
cd selenium_behave_framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (if not using Selenium)
# playwright install

# Copy environment file
cp .env.example .env
```

## Quick Start

### Running Behave BDD Tests

```bash
# Run all tests
python run_tests.py --mode behave

# Run specific tags
python run_tests.py --mode behave --tags @smoke
python run_tests.py --mode behave --tags @login @positive

# Run specific feature
python run_tests.py --mode behave --features features/login.feature

# Run in headless mode
python run_tests.py --mode behave --headless

# Dry run (validate without executing)
python run_tests.py --mode behave --dry-run
```

### Running Keyword-Driven Tests

```bash
# Create sample test data first
python run_tests.py --create-testdata

# Run keyword tests
python run_tests.py --mode keyword

# Run with specific test data
python run_tests.py --mode keyword --testdata path/to/testdata.xlsx

# Run in headless mode
python run_tests.py --mode keyword --headless --browser chrome
```

### Running Both Test Types

```bash
python run_tests.py --mode both
```

## Page Object Model (POM)

### Base Page
All page objects inherit from `BasePage` which provides:
- Element finding with waits
- Click, enter text, select operations
- Verification methods
- Screenshot capture
- JavaScript execution
- Frame/Window handling

### Example Page Object

```python
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    def login(self, username: str, password: str):
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self
```

## Behave BDD

### Feature File Example

```gherkin
@login @smoke
Feature: Login Functionality

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should be redirected to the inventory page
```

### Step Definition Example

```python
from behave import given, when, then
from pages.login_page import LoginPage

@given('I am on the login page')
def step_on_login_page(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.open()

@when('I enter username "{username}"')
def step_enter_username(context, username):
    context.login_page.enter_username(username)
```

## Keyword-Driven Testing

### Supported Keywords (40+)

| Category | Keywords |
|----------|----------|
| Navigation | NAVIGATE, REFRESH, GO_BACK, GO_FORWARD, MAXIMIZE |
| Input | ENTER, CLEAR, CLEAR_AND_ENTER, TYPE |
| Click | CLICK, DOUBLE_CLICK, RIGHT_CLICK, JS_CLICK |
| Dropdown | SELECT, SELECT_BY_VALUE, SELECT_BY_TEXT, SELECT_BY_INDEX |
| Checkbox | CHECK, UNCHECK, SELECT_RADIO |
| Verify | VERIFY_TEXT, VERIFY_TITLE, VERIFY_URL, VERIFY_ELEMENT_VISIBLE |
| Wait | WAIT, WAIT_FOR_ELEMENT, WAIT_FOR_VISIBLE, WAIT_FOR_CLICKABLE |
| Keyboard | PRESS_KEY, PRESS_ENTER, PRESS_TAB, PRESS_ESCAPE |
| Mouse | HOVER, DRAG_AND_DROP, SCROLL_TO, SCROLL_BY |
| Frame | SWITCH_TO_FRAME, SWITCH_TO_DEFAULT |
| Alert | ACCEPT_ALERT, DISMISS_ALERT, GET_ALERT_TEXT |
| Data | GET_TEXT, GET_ATTRIBUTE, STORE_TEXT, STORE_VALUE |
| Screenshot | SCREENSHOT, ELEMENT_SCREENSHOT |

### Excel Test Data Format

#### Master Sheet
| TestCaseID | Execute | ScreenFlow | Description |
|------------|---------|------------|-------------|
| TC001 | Yes | Login,Inventory | Login and view products |
| TC002 | Yes | Login,Cart,Checkout | Complete purchase |

#### Screen Sheet (e.g., "Login")
| StepNo | Keyword | Locator | LocatorValue | TestData | Description |
|--------|---------|---------|--------------|----------|-------------|
| 1 | NAVIGATE | | | https://example.com | Open URL |
| 2 | ENTER | id | username | test_user | Enter username |
| 3 | CLICK | id | login-btn | | Click login |

## Configuration

### Environment Variables (.env)

```env
# Browser
SELENIUM_BROWSER=chrome
SELENIUM_HEADLESS=False

# Timeouts
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20
PAGE_LOAD_TIMEOUT=30

# Execution
SCREENSHOT_ON_FAILURE=True
SLOW_MODE=False

# URLs
BASE_URL=https://www.saucedemo.com
```

## Reports

Reports are generated in the `reports/` directory:
- **behave_report.json** - Behave JSON report
- **keyword_test_report.html** - Keyword test HTML report
- **test_report.html** - Combined HTML report

## Browser Support

| Browser | Support |
|---------|---------|
| Chrome | Full |
| Firefox | Full |
| Edge | Full |
| Safari | Partial |

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Automation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r selenium_behave_framework/requirements.txt
      - name: Run tests
        run: |
          python selenium_behave_framework/run_tests.py --mode behave --headless
```

## Best Practices

1. **Page Objects** - Keep locators and actions in page objects
2. **Step Definitions** - Keep steps small and reusable
3. **Test Data** - Use Excel for data-driven scenarios
4. **Tags** - Use tags for test organization (@smoke, @regression)
5. **Screenshots** - Capture on failure for debugging
6. **Waits** - Use explicit waits over implicit waits
7. **Logging** - Enable detailed logging for troubleshooting

## License

MIT License
