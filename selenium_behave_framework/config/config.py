"""
Configuration module for Selenium Behave Framework
Contains all configuration settings for browser, execution, and paths
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class containing all framework settings"""

    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    ROOT_DIR = BASE_DIR.parent

    # Directory paths
    PAGES_DIR = BASE_DIR / "pages"
    FEATURES_DIR = BASE_DIR / "features"
    TEST_DATA_DIR = BASE_DIR / "test_data"
    REPORTS_DIR = BASE_DIR / "reports"
    SCREENSHOTS_DIR = BASE_DIR / "screenshots"
    LOGS_DIR = BASE_DIR / "logs"

    # Browser Configuration
    BROWSER = os.getenv("SELENIUM_BROWSER", "chrome").lower()
    HEADLESS = os.getenv("SELENIUM_HEADLESS", "False").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "20"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

    # Window settings
    WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))
    MAXIMIZE_WINDOW = os.getenv("MAXIMIZE_WINDOW", "True").lower() == "true"

    # Execution settings
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "True").lower() == "true"
    SCREENSHOT_ON_SUCCESS = os.getenv("SCREENSHOT_ON_SUCCESS", "False").lower() == "true"
    RETRY_COUNT = int(os.getenv("RETRY_COUNT", "1"))
    SLOW_MODE = os.getenv("SLOW_MODE", "False").lower() == "true"
    SLOW_MODE_DELAY = float(os.getenv("SLOW_MODE_DELAY", "0.5"))

    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_TO_FILE = os.getenv("LOG_TO_FILE", "True").lower() == "true"
    LOG_TO_CONSOLE = os.getenv("LOG_TO_CONSOLE", "True").lower() == "true"

    # Application URLs
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    API_URL = os.getenv("API_URL", "")

    # Test Data
    TEST_DATA_FILE = os.getenv("TEST_DATA_FILE", "test_data.xlsx")

    # WebDriver paths (optional - uses webdriver-manager by default)
    CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", "")
    FIREFOX_DRIVER_PATH = os.getenv("FIREFOX_DRIVER_PATH", "")
    EDGE_DRIVER_PATH = os.getenv("EDGE_DRIVER_PATH", "")

    # Remote execution settings
    REMOTE_EXECUTION = os.getenv("REMOTE_EXECUTION", "False").lower() == "true"
    SELENIUM_GRID_URL = os.getenv("SELENIUM_GRID_URL", "http://localhost:4444/wd/hub")

    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.REPORTS_DIR,
            cls.SCREENSHOTS_DIR,
            cls.LOGS_DIR,
            cls.TEST_DATA_DIR
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_test_data_path(cls) -> Path:
        """Get the full path to test data file"""
        return cls.TEST_DATA_DIR / cls.TEST_DATA_FILE

    @classmethod
    def get_screenshot_path(cls, name: str) -> Path:
        """Get the full path for a screenshot"""
        return cls.SCREENSHOTS_DIR / f"{name}.png"

    @classmethod
    def get_log_path(cls) -> Path:
        """Get the full path for log file"""
        return cls.LOGS_DIR / "test_execution.log"


# Create directories on import
Config.create_directories()
