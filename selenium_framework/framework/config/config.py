"""
Configuration module for Selenium Test Automation Framework.
Contains all configurable parameters for test execution.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Central configuration class for the framework."""

    # Base paths
    BASE_DIR = Path(__file__).parent.parent.parent
    TEST_DATA_DIR = BASE_DIR / "test_data"
    REPORTS_DIR = BASE_DIR / "reports"
    SCREENSHOTS_DIR = BASE_DIR / "screenshots"
    LOGS_DIR = BASE_DIR / "logs"

    # Browser Configuration
    BROWSER = os.getenv("BROWSER", "chrome")  # chrome, firefox, edge
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    SCRIPT_TIMEOUT = int(os.getenv("SCRIPT_TIMEOUT", "30"))

    # Window Configuration
    WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))
    MAXIMIZE_WINDOW = os.getenv("MAXIMIZE_WINDOW", "True").lower() == "true"

    # Test Data Configuration
    TEST_DATA_FILE = os.getenv("TEST_DATA_FILE", "TestData.xlsx")
    TEST_DATA_PATH = TEST_DATA_DIR / TEST_DATA_FILE
    MASTER_SHEET_NAME = os.getenv("MASTER_SHEET_NAME", "Master")

    # Execution Settings
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "True").lower() == "true"
    SCREENSHOT_ON_SUCCESS = os.getenv("SCREENSHOT_ON_SUCCESS", "True").lower() == "true"
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "1"))
    DEFAULT_WAIT = int(os.getenv("DEFAULT_WAIT", "10"))

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / "test_execution.log"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    # Report Configuration
    REPORT_FILE = REPORTS_DIR / "test_report.html"
    REPORT_TITLE = os.getenv("REPORT_TITLE", "Selenium Test Automation Report")

    # Application URLs
    BASE_URL = os.getenv("BASE_URL", "https://example.com")

    # WebDriver Configuration
    CHROME_OPTIONS = [
        "--disable-blink-features=AutomationControlled",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]

    FIREFOX_OPTIONS = [
        "--disable-blink-features=AutomationControlled"
    ]

    EDGE_OPTIONS = [
        "--disable-blink-features=AutomationControlled",
        "--disable-extensions"
    ]

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist."""
        for directory in [cls.TEST_DATA_DIR, cls.REPORTS_DIR,
                         cls.SCREENSHOTS_DIR, cls.LOGS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_screenshot_path(cls, filename):
        """Get full path for screenshot file."""
        return cls.SCREENSHOTS_DIR / f"{filename}.png"

    @classmethod
    def get_config_summary(cls):
        """Return a summary of current configuration."""
        return {
            "Browser": cls.BROWSER,
            "Headless": cls.HEADLESS,
            "Maximize Window": cls.MAXIMIZE_WINDOW,
            "Implicit Wait": cls.IMPLICIT_WAIT,
            "Page Load Timeout": cls.PAGE_LOAD_TIMEOUT,
            "Test Data Path": str(cls.TEST_DATA_PATH),
            "Screenshots": f"Failure={cls.SCREENSHOT_ON_FAILURE}, Success={cls.SCREENSHOT_ON_SUCCESS}",
            "Log Level": cls.LOG_LEVEL
        }
