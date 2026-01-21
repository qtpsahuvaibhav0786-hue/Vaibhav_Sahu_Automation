"""
Logger Module.
Provides color-coded logging for test execution with file and console output.
"""

import logging
import colorlog
from pathlib import Path
from framework.config.config import Config


class Logger:
    """
    Singleton logger class for consistent logging across the framework.
    Provides both console (colored) and file logging.
    """

    _instance = None

    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize logger with console and file handlers."""
        if self._initialized:
            return

        self._initialized = True
        self.logger = logging.getLogger("SeleniumFramework")
        self.logger.setLevel(getattr(logging, Config.LOG_LEVEL))

        # Clear existing handlers
        self.logger.handlers.clear()

        # Console handler with colors
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)-8s%(reset)s - %(message)s",
            datefmt=Config.LOG_DATE_FORMAT,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )

        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler
        Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(Config.LOG_FILE, mode='w', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter(
            Config.LOG_FORMAT,
            datefmt=Config.LOG_DATE_FORMAT
        )

        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        """Log debug message."""
        self.logger.debug(message)

    def info(self, message):
        """Log info message."""
        self.logger.info(message)

    def warning(self, message):
        """Log warning message."""
        self.logger.warning(message)

    def error(self, message):
        """Log error message."""
        self.logger.error(message)

    def critical(self, message):
        """Log critical message."""
        self.logger.critical(message)

    def success(self, message):
        """Log success message (using info level with green color)."""
        # Create a temporary handler for success messages
        console_handler = colorlog.StreamHandler()
        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - SUCCESS %(reset)s - %(message)s",
            datefmt=Config.LOG_DATE_FORMAT,
            log_colors={'INFO': 'green'}
        )
        console_handler.setFormatter(console_formatter)

        # Temporarily replace handlers
        original_handlers = self.logger.handlers.copy()
        self.logger.handlers.clear()
        self.logger.addHandler(console_handler)

        # Also add file handler
        for handler in original_handlers:
            if isinstance(handler, logging.FileHandler):
                self.logger.addHandler(handler)

        self.logger.info(message)

        # Restore original handlers
        self.logger.handlers = original_handlers

    def test_start(self, test_id, description):
        """
        Log test case start.

        Args:
            test_id (str): Test case ID
            description (str): Test case description
        """
        self.info("=" * 80)
        self.info(f"TEST CASE: {test_id}")
        self.info(f"DESCRIPTION: {description}")
        self.info("=" * 80)

    def test_end(self, passed):
        """
        Log test case end.

        Args:
            passed (bool): Whether test passed or failed
        """
        if passed:
            self.success("✓ TEST CASE PASSED")
        else:
            self.error("✗ TEST CASE FAILED")
        self.info("=" * 80 + "\n")

    def keyword_execution(self, step_number, keyword, field_name, locator, value):
        """
        Log keyword execution details.

        Args:
            step_number (int): Step number
            keyword (str): Keyword being executed
            field_name (str): Field name
            locator (str): Element locator
            value (str): Value/data for the keyword
        """
        # Truncate long locators for readability
        display_locator = locator if len(locator) <= 50 else locator[:47] + "..."
        display_value = value if len(value) <= 30 else value[:27] + "..."

        self.info(f"  Step {step_number}: {keyword}")
        self.info(f"    Field: {field_name}")

        if locator:
            self.info(f"    Locator: {display_locator}")

        if value:
            self.info(f"    Value: {display_value}")

    def step_result(self, success, message):
        """
        Log step execution result.

        Args:
            success (bool): Whether step succeeded
            message (str): Result message
        """
        if success:
            # Use cyan color for successful steps
            console_handler = colorlog.StreamHandler()
            console_formatter = colorlog.ColoredFormatter(
                "%(log_color)s    ✓ %(message)s%(reset)s",
                log_colors={'INFO': 'cyan'}
            )
            console_handler.setFormatter(console_formatter)

            original_handlers = self.logger.handlers.copy()
            self.logger.handlers.clear()
            self.logger.addHandler(console_handler)

            for handler in original_handlers:
                if isinstance(handler, logging.FileHandler):
                    self.logger.addHandler(handler)

            self.logger.info(message)
            self.logger.handlers = original_handlers
        else:
            self.error(f"    ✗ {message}")

    def separator(self, char="=", length=80):
        """
        Log separator line.

        Args:
            char (str): Character to use for separator
            length (int): Length of separator
        """
        self.info(char * length)

    def section(self, title):
        """
        Log section header.

        Args:
            title (str): Section title
        """
        self.separator()
        self.info(title)
        self.separator()
