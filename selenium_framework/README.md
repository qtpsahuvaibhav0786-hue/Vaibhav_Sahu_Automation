# Selenium Python Test Automation Framework

A comprehensive keyword-driven test automation framework built with Selenium WebDriver and Python. This framework enables non-technical users to create and execute automated tests using Excel spreadsheets, without writing any code.

## Features

- **Keyword-Driven Testing**: Execute tests using simple keywords in Excel
- **Multi-Browser Support**: Chrome, Firefox, and Edge browsers
- **Excel-Based Test Data**: Manage test cases and data in Excel files
- **Automatic Screenshot Capture**: Screenshots on test pass/fail
- **Beautiful HTML Reports**: Detailed test execution reports with statistics
- **Color-Coded Logging**: Easy-to-read console output with file logging
- **Flexible Configuration**: Environment-based configuration using `.env` files
- **Screen Flow Support**: Execute multi-screen test scenarios
- **Automatic Driver Management**: WebDriver Manager handles browser drivers
- **Comprehensive Keywords**: 45+ built-in keywords for web automation

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Excel File Format](#excel-file-format)
- [Available Keywords](#available-keywords)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Reports and Logs](#reports-and-logs)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the repository**

2. **Navigate to the selenium_framework directory**
   ```bash
   cd selenium_framework
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create sample test data**
   ```bash
   python create_sample_testdata.py
   ```

5. **Verify installation**
   ```bash
   python run_tests.py --help
   ```

## Quick Start

### 1. Generate Sample Test Data

```bash
python create_sample_testdata.py
```

This creates a sample `TestData.xlsx` file with:
- Master sheet for test case management
- LoginScreen with sample login tests
- DashboardScreen with verification tests

### 2. Run Tests

```bash
# Run all test cases marked as "Yes" in Master sheet
python run_tests.py

# Run a specific test case
python run_tests.py --test-case TC001

# Use a different Excel file
python run_tests.py --data-file path/to/CustomData.xlsx
```

### 3. View Results

- **HTML Report**: `reports/test_report.html` (open in browser)
- **Logs**: `logs/test_execution.log`
- **Screenshots**: `screenshots/` directory

## Project Structure

```
selenium_framework/
├── framework/                      # Core framework package
│   ├── config/
│   │   └── config.py              # Configuration management
│   ├── core/
│   │   ├── selenium_driver.py     # WebDriver wrapper
│   │   ├── excel_reader.py        # Excel file parser
│   │   └── test_executor.py       # Test execution orchestrator
│   ├── keywords/
│   │   └── keyword_engine.py      # Keyword implementations
│   └── utils/
│       ├── logger.py              # Logging utility
│       └── report_generator.py    # HTML report generator
├── test_data/                     # Excel test data files
│   └── TestData.xlsx
├── reports/                       # HTML test reports
├── logs/                          # Execution logs
├── screenshots/                   # Test screenshots
├── run_tests.py                   # Main test runner
├── create_sample_testdata.py     # Sample data generator
├── requirements.txt               # Python dependencies
├── .env                          # Environment configuration
└── README.md                     # This file
```

## Excel File Format

### Master Sheet

Controls which test cases to execute.

| TestCaseID | Execute | ScreenFlow              | Description                    |
|------------|---------|-------------------------|--------------------------------|
| TC001      | Yes     | LoginScreen             | Valid login test               |
| TC002      | Yes     | LoginScreen             | Invalid login test             |
| TC003      | Yes     | LoginScreen,Dashboard   | Login and verify dashboard     |
| TC004      | No      | LoginScreen             | Locked user test (disabled)    |

**Columns:**
- `TestCaseID`: Unique identifier for the test case
- `Execute`: "Yes" to run, "No" to skip
- `ScreenFlow`: Comma-separated list of screen sheets to execute
- `Description`: Test case description

### Screen Sheets

Each screen has its own sheet with this structure:

**Row 1: Field Names** (Header row with field identifiers)
```
| URL | Username | Password | LoginButton | ErrorMessage |
```

**Row 2: Locators** (Element locators for each field)
```
| https://www.example.com | id=username | id=password | //button[@type='submit'] | //div[@class='error'] |
```

**Row 3: Keywords** (Actions to perform)
```
| NAVIGATE | ENTER | ENTER | CLICK | VERIFY_TEXT |
```

**Row 4: Values** (Test data for keywords)
```
| | admin | password123 | | Login successful |
```

**Notes:**
- Rows 3 & 4 form one test case (keyword-value pair)
- Rows 5 & 6 form another test case, and so on
- Each test case uses 2 rows: Keywords row + Values row

### Locator Formats

The framework supports multiple locator strategies:

```
XPath:           //div[@id='example']
ID:              id=username
CSS:             css=.class-name
Name:            name=email
Class:           class=button-primary
Link Text:       link=Click Here
Partial Link:    partial_link=Click
Tag:             tag=button
```

## Available Keywords

### Navigation Keywords

| Keyword      | Description                    | Example Value       |
|--------------|--------------------------------|---------------------|
| NAVIGATE     | Navigate to URL                | https://example.com |
| REFRESH      | Refresh current page           |                     |
| GO_BACK      | Navigate back                  |                     |
| GO_FORWARD   | Navigate forward               |                     |

### Input Keywords

| Keyword      | Description                    | Example Value       |
|--------------|--------------------------------|---------------------|
| ENTER        | Enter text in element          | Hello World         |
| CLEAR        | Clear text from element        |                     |
| SELECT       | Select dropdown option         | Option 1            |

### Click Keywords

| Keyword       | Description                   | Example Value       |
|---------------|-------------------------------|---------------------|
| CLICK         | Click element                 |                     |
| DOUBLE_CLICK  | Double click element          |                     |
| RIGHT_CLICK   | Right click element           |                     |

### Verification Keywords

| Keyword        | Description                  | Example Value       |
|----------------|------------------------------|---------------------|
| VERIFY_TEXT    | Verify element contains text | Expected Text       |
| VERIFY_TITLE   | Verify page title            | Page Title          |
| VERIFY_URL     | Verify current URL           | /dashboard          |
| VERIFY_ELEMENT | Verify element exists        |                     |

### Wait Keywords

| Keyword          | Description                 | Example Value       |
|------------------|-----------------------------|---------------------|
| WAIT             | Wait for specified seconds  | 5                   |
| WAIT_FOR_ELEMENT | Wait for element visibility | 10                  |

### Checkbox/Radio Keywords

| Keyword      | Description              | Example Value       |
|--------------|--------------------------|---------------------|
| CHECK        | Check checkbox/radio     |                     |
| UNCHECK      | Uncheck checkbox         |                     |

### Mouse Interaction Keywords

| Keyword      | Description              | Example Value       |
|--------------|--------------------------|---------------------|
| HOVER        | Hover over element       |                     |
| SCROLL_TO    | Scroll to element        |                     |
| DRAG_DROP    | Drag and drop            | target_locator      |

### Keyboard Keywords

| Keyword      | Description              | Example Value       |
|--------------|--------------------------|---------------------|
| PRESS_KEY    | Press keyboard key       | ENTER               |

**Supported keys**: ENTER, TAB, ESC, SPACE, BACKSPACE, DELETE, ARROW_UP, ARROW_DOWN, ARROW_LEFT, ARROW_RIGHT

### Frame Keywords

| Keyword           | Description                    | Example Value       |
|-------------------|--------------------------------|---------------------|
| SWITCH_TO_FRAME   | Switch to iframe               | frame_name or index |
| SWITCH_TO_DEFAULT | Switch to default content      |                     |

### Alert Keywords

| Keyword        | Description              | Example Value       |
|----------------|--------------------------|---------------------|
| ACCEPT_ALERT   | Accept alert dialog      |                     |
| DISMISS_ALERT  | Dismiss alert dialog     |                     |
| GET_ALERT_TEXT | Get alert text           |                     |

### Window/Tab Keywords

| Keyword        | Description              | Example Value       |
|----------------|--------------------------|---------------------|
| CLOSE_TAB      | Close current tab        |                     |
| SWITCH_WINDOW  | Switch to window         | 0 (index) or handle |

### Information Retrieval Keywords

| Keyword         | Description              | Example Value       |
|-----------------|--------------------------|---------------------|
| GET_TEXT        | Get element text         |                     |
| GET_ATTRIBUTE   | Get element attribute    | href                |
| IS_VISIBLE      | Check if visible         |                     |
| IS_ENABLED      | Check if enabled         |                     |
| IS_SELECTED     | Check if selected        |                     |

### JavaScript Keywords

| Keyword         | Description              | Example Value       |
|-----------------|--------------------------|---------------------|
| EXECUTE_SCRIPT  | Execute JavaScript       | alert('Hello');     |

## Configuration

### Environment Variables (.env)

```bash
# Browser Configuration
BROWSER=chrome              # chrome, firefox, edge
HEADLESS=False             # True for headless mode

# Timeouts (seconds)
IMPLICIT_WAIT=10
PAGE_LOAD_TIMEOUT=30
SCRIPT_TIMEOUT=30

# Window Configuration
WINDOW_WIDTH=1920
WINDOW_HEIGHT=1080
MAXIMIZE_WINDOW=True

# Test Data
TEST_DATA_FILE=TestData.xlsx
MASTER_SHEET_NAME=Master

# Screenshots
SCREENSHOT_ON_FAILURE=True
SCREENSHOT_ON_SUCCESS=True

# Logging
LOG_LEVEL=INFO             # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Application
BASE_URL=https://www.saucedemo.com
```

### Programmatic Configuration

Edit `framework/config/config.py` for advanced configuration:
- Chrome/Firefox/Edge options
- Custom driver settings
- Report customization

## Running Tests

### Basic Execution

```bash
# Run all test cases
python run_tests.py

# Run specific test case
python run_tests.py --test-case TC001

# Use custom Excel file
python run_tests.py --data-file custom_tests.xlsx
```

### Environment-Specific Runs

```bash
# Run in headless mode
HEADLESS=True python run_tests.py

# Use Firefox
BROWSER=firefox python run_tests.py

# Debug mode with verbose logging
LOG_LEVEL=DEBUG python run_tests.py
```

### CI/CD Integration

```bash
# Run in CI environment
HEADLESS=True BROWSER=chrome python run_tests.py
EXIT_CODE=$?
exit $EXIT_CODE
```

## Reports and Logs

### HTML Report

Located at: `reports/test_report.html`

Features:
- Test execution summary with statistics
- Pass/fail counts and pass rate
- Detailed test results table
- Screenshot links for each test
- Execution duration and timestamps
- Beautiful responsive design

### Log File

Located at: `logs/test_execution.log`

Contains:
- Detailed execution steps
- Keyword execution logs
- Element locator information
- Error messages and stack traces
- Timestamps for all operations

### Screenshots

Located at: `screenshots/` directory

Naming convention: `TestCaseID_STATUS_TIMESTAMP.png`
- `TC001_PASS_20240115_143022.png`
- `TC002_FAIL_20240115_143045.png`

## Advanced Usage

### Creating Custom Keywords

Add new keywords to `framework/keywords/keyword_engine.py`:

```python
def _custom_keyword(self, locator, value):
    """Custom keyword implementation."""
    try:
        # Your implementation here
        return True, "Success message"
    except Exception as e:
        return False, f"Error: {str(e)}"

# Register in keyword_map
self.keyword_map["CUSTOM_KEYWORD"] = self._custom_keyword
```

### Multi-Screen Test Flows

Chain multiple screens in the Master sheet:

```
ScreenFlow: LoginScreen,DashboardScreen,ProfileScreen
```

The framework will execute screens in sequence using the same browser session.

### Data-Driven Testing

Create multiple test cases by adding more keyword-value row pairs in screen sheets:

```
Row 3-4:  Test Case 1 (Keywords + Values)
Row 5-6:  Test Case 2 (Keywords + Values)
Row 7-8:  Test Case 3 (Keywords + Values)
```

### Custom Locator Strategies

The framework auto-detects locator types:
- Starts with `//` or `(//` → XPath
- Starts with `id=` → ID
- Starts with `css=` → CSS Selector
- Starts with `name=` → Name
- Starts with `class=` → Class Name

## Troubleshooting

### Common Issues

**1. Browser driver not found**
```
Solution: WebDriver Manager should auto-download drivers.
If it fails, check your internet connection.
```

**2. Element not found**
```
Solution:
- Verify locator in browser DevTools
- Increase wait time in .env (IMPLICIT_WAIT)
- Use WAIT_FOR_ELEMENT keyword before interacting
```

**3. Excel file not loading**
```
Solution:
- Check file path in .env (TEST_DATA_FILE)
- Ensure Excel file is closed (not open in Excel)
- Verify Excel file format matches requirements
```

**4. Tests running but no report generated**
```
Solution:
- Check write permissions on reports/ directory
- Review logs/test_execution.log for errors
- Ensure all tests completed execution
```

**5. Screenshots not saving**
```
Solution:
- Check write permissions on screenshots/ directory
- Verify SCREENSHOT_ON_FAILURE/SUCCESS in .env
- Ensure browser is running (not headless for debugging)
```

### Debug Mode

Enable detailed logging:

```bash
# In .env file
LOG_LEVEL=DEBUG

# Or via command line
LOG_LEVEL=DEBUG python run_tests.py
```

### Getting Help

1. Check the logs: `logs/test_execution.log`
2. Review the HTML report: `reports/test_report.html`
3. Enable DEBUG logging for more details
4. Verify Excel file format matches documentation

## Best Practices

### 1. Test Design
- Keep test cases atomic and independent
- Use descriptive test case IDs and descriptions
- Group related screens logically
- Avoid test dependencies

### 2. Locators
- Prefer ID and CSS selectors over XPath
- Use unique, stable locators
- Avoid index-based XPath
- Test locators in browser DevTools

### 3. Test Data
- Use meaningful field names
- Keep test data realistic
- Separate positive and negative tests
- Document test data sources

### 4. Maintenance
- Review and update locators regularly
- Archive old test data
- Clean up screenshots periodically
- Keep dependencies updated

### 5. CI/CD
- Run in headless mode
- Set appropriate timeouts
- Archive reports and logs
- Use exit codes for pipeline decisions

## Framework Architecture

```
┌─────────────────┐
│   run_tests.py  │  Entry Point
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  TestExecutor   │  Orchestrates test execution
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌─────────┐ ┌────────┐ ┌─────────┐ ┌────────────┐
│Excel    │ │Selenium│ │Keyword  │ │Report      │
│Reader   │ │Driver  │ │Engine   │ │Generator   │
└─────────┘ └────────┘ └─────────┘ └────────────┘
```

## Contributing

To extend the framework:

1. Add new keywords in `keyword_engine.py`
2. Update configuration in `config.py`
3. Modify report template in `report_generator.py`
4. Document changes in README.md

## License

This framework is provided as-is for educational and commercial use.

## Support

For issues or questions:
- Review this README thoroughly
- Check the troubleshooting section
- Examine log files for error details
- Verify Excel file format

---

**Happy Testing! 🚀**
