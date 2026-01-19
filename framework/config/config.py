"""
Configuration module for the keyword-driven test automation framework
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEST_DATA_DIR = BASE_DIR / "test_data"
REPORTS_DIR = BASE_DIR / "reports"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for directory in [TEST_DATA_DIR, REPORTS_DIR, SCREENSHOTS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Browser configuration
BROWSER_CONFIG = {
    "browser": os.getenv("BROWSER", "chromium"),  # chromium, firefox, webkit
    "headless": os.getenv("HEADLESS", "False").lower() == "true",
    "slow_mo": int(os.getenv("SLOW_MO", "0")),
    "timeout": int(os.getenv("TIMEOUT", "30000")),
    "viewport": {
        "width": int(os.getenv("VIEWPORT_WIDTH", "1920")),
        "height": int(os.getenv("VIEWPORT_HEIGHT", "1080"))
    }
}

# Test data configuration
TEST_DATA_CONFIG = {
    "master_sheet_name": "MasterSheet",
    "test_data_file": str(TEST_DATA_DIR / "TestData.xlsx")
}

# Execution configuration
EXECUTION_CONFIG = {
    "screenshot_on_failure": True,
    "screenshot_on_success": False,
    "video_record": False,
    "max_retries": int(os.getenv("MAX_RETRIES", "1")),
    "wait_time": int(os.getenv("DEFAULT_WAIT", "10"))
}

# Logging configuration
LOGGING_CONFIG = {
    "log_level": os.getenv("LOG_LEVEL", "INFO"),
    "log_file": str(LOGS_DIR / "test_execution.log"),
    "console_output": True
}

# Report configuration
REPORT_CONFIG = {
    "report_title": "Keyword Driven Test Automation Report",
    "report_name": "test_report.html",
    "report_path": str(REPORTS_DIR)
}
