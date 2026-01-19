# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install
```

### 2. Create Test Data
```bash
python create_sample_testdata.py
```

### 3. Run Tests
```bash
python run_tests.py
```

## View Results

- **Report**: Open `reports/test_report.html` in browser
- **Logs**: Check `logs/test_execution.log`
- **Screenshots**: View in `screenshots/` folder

## Customize Your Tests

### Step 1: Open Excel File
Open `test_data/TestData.xlsx`

### Step 2: Edit Master Sheet
Select which tests to run:
```
TestCaseID | Execute | ScreenFlow        | Description
TC001      | Yes     | LoginScreen       | My test case
```

### Step 3: Edit Screen Sheets
Update fields, locators, and test data:
```
Row 1: Field names (Username, Password, etc.)
Row 2: XPath locators
Row 3: Keywords (ENTER, CLICK, etc.)
Row 4: Values (test data)
```

## Common Keywords

- **NAVIGATE** - Go to URL
- **ENTER** - Type text
- **CLICK** - Click element
- **VERIFY_TEXT** - Check text
- **WAIT** - Wait seconds
- **SELECT** - Select dropdown

See README.md for full keyword list.

## Configuration

Edit `.env` file:
```env
BROWSER=chromium      # chromium, firefox, webkit
HEADLESS=False       # True for headless mode
TIMEOUT=30000        # Timeout in milliseconds
```

## Need Help?

1. Check `README.md` for detailed documentation
2. Review sample test data in `test_data/TestData.xlsx`
3. Check logs in `logs/test_execution.log`

**Happy Testing!** 🚀
