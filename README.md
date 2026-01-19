# Keyword Driven Test Automation Framework
## Playwright + Python

A comprehensive keyword-driven test automation framework built with Playwright and Python. This framework allows you to write test cases in Excel sheets using keywords, making it easy for non-technical users to create and maintain test cases.

---

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Excel Test Data Structure](#excel-test-data-structure)
- [Supported Keywords](#supported-keywords)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Reports and Logs](#reports-and-logs)
- [Advanced Usage](#advanced-usage)

---

## Features

✅ **Keyword-Driven Testing** - Write test cases using simple keywords in Excel
✅ **Excel-Based Test Data** - Manage test cases and data in Excel sheets
✅ **Master Sheet Control** - Select which test cases to execute
✅ **Screen Flow Support** - Define multi-screen test flows
✅ **Playwright Integration** - Fast, reliable browser automation
✅ **Multi-Browser Support** - Chromium, Firefox, WebKit
✅ **Detailed Logging** - Color-coded console logs and file logs
✅ **HTML Reports** - Beautiful, comprehensive test reports
✅ **Screenshots** - Auto-capture on failure/success
✅ **Easy Configuration** - Environment-based settings via .env

---

## Project Structure

```
Vaibhav_Sahu_Automation/
├── framework/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── browser_manager.py      # Playwright browser operations
│   │   ├── excel_reader.py         # Excel data parser
│   │   └── test_executor.py        # Main test execution engine
│   ├── keywords/
│   │   ├── __init__.py
│   │   └── keyword_engine.py       # Keyword execution logic
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py               # Framework configuration
│   └── utils/
│       ├── __init__.py
│       ├── logger.py               # Logging utility
│       └── report_generator.py    # HTML report generator
├── test_data/
│   └── TestData.xlsx               # Test data Excel file
├── reports/                        # Generated HTML reports
├── screenshots/                    # Test screenshots
├── logs/                          # Execution logs
├── .env                           # Environment configuration
├── requirements.txt               # Python dependencies
├── create_sample_testdata.py     # Script to create sample Excel
└── run_tests.py                  # Main execution script
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Repository

```bash
cd Vaibhav_Sahu_Automation
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Install Playwright Browsers

```bash
playwright install
```

This will download Chromium, Firefox, and WebKit browsers.

---

## Quick Start

### 1. Create Sample Test Data

Run the following command to create a sample Excel test data file:

```bash
python create_sample_testdata.py
```

This creates `test_data/TestData.xlsx` with sample test cases.

### 2. Run Tests

```bash
python run_tests.py
```

### 3. View Report

After execution, open the HTML report:
- Location: `reports/test_report.html`
- Open in any browser to view detailed results

---

## Excel Test Data Structure

### Master Sheet

The Master Sheet controls test execution and defines screen flows.

**Structure:**

| TestCaseID | Execute | ScreenFlow                    | Description                |
|------------|---------|-------------------------------|----------------------------|
| TC001      | Yes     | LoginScreen                   | Valid login test case      |
| TC002      | No      | LoginScreen                   | Invalid login test case    |
| TC003      | Yes     | LoginScreen,DashboardScreen   | Login and dashboard flow   |

**Columns:**
- **TestCaseID**: Unique identifier for the test case
- **Execute**: "Yes" or "Y" to run the test case, "No" to skip
- **ScreenFlow**: Comma-separated list of screens (e.g., "LoginScreen,DashboardScreen")
- **Description**: Brief description of the test case

### Screen Sheets

Each screen has its own worksheet with field definitions and test data.

**Structure:**

#### Row 1: Field Names (Headers)
```
| URL | Username | Password | LoginButton | ErrorMessage |
```

#### Row 2: XPath/Locators
```
| https://example.com | //input[@id='username'] | //input[@id='password'] | //button[@id='login'] | //div[@class='error'] |
```

#### Row 3: Keywords (Test Case 1)
```
| NAVIGATE | ENTER | ENTER | CLICK | VERIFY_TEXT |
```

#### Row 4: Values (Test Case 1)
```
|  | admin@test.com | Admin@123 |  |  |
```

#### Row 5-6: Next Test Case (2 rows per test case)
Continue with keywords and values for additional test cases...

**Format Rules:**
- **Row 1**: Field names
- **Row 2**: XPath/CSS selectors for each field
- **Row 3+**: Test data in pairs (keyword row + value row)
- **2 rows per test case**: First row = keywords, Second row = values

---

## Supported Keywords

### Navigation Keywords
- **NAVIGATE** - Navigate to URL
  ```
  Locator: URL
  Value: (empty)
  ```

### Input Keywords
- **ENTER** - Enter text in input field
  ```
  Locator: //input[@id='username']
  Value: admin@test.com
  ```
- **CLEAR** - Clear input field
- **SELECT** - Select option from dropdown
  ```
  Locator: //select[@id='country']
  Value: USA
  ```

### Click Keywords
- **CLICK** - Click on element
- **DOUBLE_CLICK** - Double click element
- **RIGHT_CLICK** - Right click element

### Verification Keywords
- **VERIFY_TEXT** - Verify element text contains expected text
  ```
  Locator: //div[@class='message']
  Value: Welcome
  ```
- **VERIFY_TITLE** - Verify page title
  ```
  Locator: Expected Title
  Value: (empty)
  ```
- **VERIFY_URL** - Verify current URL contains expected text
  ```
  Locator: /dashboard
  Value: (empty)
  ```

### Wait Keywords
- **WAIT** - Wait for specified seconds
  ```
  Locator: 5
  Value: (empty)
  ```
- **WAIT_FOR_ELEMENT** - Wait for element to be visible
  ```
  Locator: //div[@id='content']
  Value: 10 (timeout in seconds)
  ```

### Checkbox/Radio Keywords
- **CHECK** - Check checkbox
- **UNCHECK** - Uncheck checkbox

### Mouse Keywords
- **HOVER** - Hover over element
- **SCROLL_TO** - Scroll to element

### Keyboard Keywords
- **PRESS_KEY** - Press keyboard key
  ```
  Locator: Enter
  Value: (empty)
  ```

### Frame Keywords
- **SWITCH_TO_FRAME** - Switch to iframe
- **SWITCH_TO_DEFAULT** - Switch back to default content

### Alert Keywords
- **ACCEPT_ALERT** - Accept alert dialog
- **DISMISS_ALERT** - Dismiss alert dialog

### Browser Keywords
- **REFRESH** - Refresh current page
- **GO_BACK** - Navigate back
- **GO_FORWARD** - Navigate forward
- **CLOSE_TAB** - Close current tab

### Information Keywords
- **GET_TEXT** - Get element text
- **IS_VISIBLE** - Check if element is visible
- **IS_ENABLED** - Check if element is enabled

---

## Configuration

Edit the `.env` file to configure framework settings:

```env
# Browser Configuration
BROWSER=chromium              # chromium, firefox, webkit
HEADLESS=False               # True for headless mode
SLOW_MO=500                  # Slow down actions by milliseconds
TIMEOUT=30000                # Default timeout in milliseconds
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080

# Execution Configuration
MAX_RETRIES=1
DEFAULT_WAIT=10
LOG_LEVEL=INFO               # DEBUG, INFO, WARNING, ERROR

# Application URLs
BASE_URL=https://example.com
```

---

## Running Tests

### Basic Execution

```bash
python run_tests.py
```

### Custom Test Data File

```bash
python run_tests.py --testdata path/to/your/TestData.xlsx
```

### Specify Browser

```bash
python run_tests.py --browser firefox
python run_tests.py --browser webkit
```

### Headless Mode

```bash
python run_tests.py --headless
```

### Combined Options

```bash
python run_tests.py --testdata test_data/MyTests.xlsx --browser chromium --headless
```

---

## Reports and Logs

### HTML Report
- **Location**: `reports/test_report.html`
- **Contains**:
  - Test summary with pass/fail counts
  - Pass percentage
  - Execution duration
  - Detailed test results table
  - Screenshots for failed tests

### Logs
- **Location**: `logs/test_execution.log`
- **Format**: Timestamped logs with log levels
- **Console**: Color-coded logs for easy reading

### Screenshots
- **Location**: `screenshots/`
- **Naming**: `TestCaseID_ScreenName_Status_Timestamp.png`
- **Auto-capture**: On failure (configurable for success too)

---

## Advanced Usage

### Adding New Keywords

Edit `framework/keywords/keyword_engine.py` and add your custom keyword:

```python
def my_custom_keyword(self, locator, value=""):
    """Custom keyword description"""
    try:
        # Your implementation
        return True, "Success message"
    except Exception as e:
        return False, f"Error: {str(e)}"
```

Then add it to the `keyword_map` dictionary in `execute_keyword()` method.

### Creating New Screen Sheets

1. Open `test_data/TestData.xlsx`
2. Create a new sheet with your screen name (e.g., "CheckoutScreen")
3. Add field names in Row 1
4. Add XPath/locators in Row 2
5. Add test cases from Row 3 onwards (2 rows per test case)
6. Update Master Sheet with test cases using your new screen

### Modifying Browser Settings

Edit `framework/config/config.py`:

```python
BROWSER_CONFIG = {
    "browser": "chromium",
    "headless": False,
    "slow_mo": 500,
    "timeout": 30000,
    "viewport": {"width": 1920, "height": 1080}
}
```

---

## Troubleshooting

### Issue: Excel file not found
**Solution**: Run `python create_sample_testdata.py` to create the test data file.

### Issue: Playwright browsers not found
**Solution**: Run `playwright install` to download browsers.

### Issue: Module not found errors
**Solution**: Install dependencies with `pip install -r requirements.txt`

### Issue: Tests not executing
**Solution**: Check Master Sheet - ensure "Execute" column has "Yes" or "Y" for test cases.

### Issue: Locator not found
**Solution**:
- Verify XPath/CSS selector in Row 2 of screen sheet
- Check if element exists on the page
- Add wait time using WAIT_FOR_ELEMENT keyword

---

## Best Practices

1. **Use Descriptive Test Case IDs**: Use meaningful IDs like "LOGIN_VALID_001" instead of "TC001"

2. **Organize Screen Flows**: Break complex flows into smaller, reusable screens

3. **Add Wait Keywords**: Use WAIT_FOR_ELEMENT before interacting with dynamic elements

4. **Use Verification Keywords**: Add VERIFY_TEXT, VERIFY_TITLE to validate test results

5. **Maintain Locators**: Keep XPath/CSS selectors in Row 2 updated when UI changes

6. **Use Relative XPath**: Prefer relative XPath over absolute for better maintainability

7. **Add Descriptions**: Use descriptive test case descriptions in Master Sheet

8. **Review Reports**: Always check HTML reports after execution

---

## Contributing

Feel free to extend this framework by:
- Adding new keywords
- Improving error handling
- Adding more reporting formats
- Enhancing Excel parsing capabilities

---

## Support

For issues or questions:
- Check logs in `logs/test_execution.log`
- Review screenshots in `screenshots/`
- Check HTML report in `reports/test_report.html`

---

## License

This framework is provided as-is for testing purposes.

---

**Happy Testing! 🚀**
