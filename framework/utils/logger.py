"""
Logger module for the keyword-driven test automation framework
"""
import logging
import colorlog
from datetime import datetime
from framework.config.config import LOGGING_CONFIG

class Logger:
    """Custom logger class with color-coded console output"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        """Initialize the logger with file and console handlers"""
        self.logger = logging.getLogger("KeywordFramework")
        self.logger.setLevel(getattr(logging, LOGGING_CONFIG["log_level"]))

        # Remove existing handlers
        if self.logger.handlers:
            self.logger.handlers.clear()

        # File handler
        file_handler = logging.FileHandler(LOGGING_CONFIG["log_file"])
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)

        # Console handler with colors
        if LOGGING_CONFIG["console_output"]:
            console_handler = colorlog.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = colorlog.ColoredFormatter(
                '%(log_color)s%(asctime)s - %(levelname)-8s%(reset)s %(blue)s%(message)s',
                datefmt='%H:%M:%S',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                }
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

        self.logger.addHandler(file_handler)

    def info(self, message):
        """Log info message"""
        self.logger.info(message)

    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)

    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)

    def error(self, message):
        """Log error message"""
        self.logger.error(message)

    def critical(self, message):
        """Log critical message"""
        self.logger.critical(message)

    def test_start(self, test_name):
        """Log test start"""
        self.logger.info(f"{'='*80}")
        self.logger.info(f"Starting Test: {test_name}")
        self.logger.info(f"{'='*80}")

    def test_end(self, test_name, status):
        """Log test end"""
        self.logger.info(f"{'='*80}")
        self.logger.info(f"Test Completed: {test_name} - Status: {status}")
        self.logger.info(f"{'='*80}\n")

    def keyword_execution(self, keyword, element, value=""):
        """Log keyword execution"""
        if value:
            self.logger.info(f"Executing: {keyword} on '{element}' with value '{value}'")
        else:
            self.logger.info(f"Executing: {keyword} on '{element}'")

    def step_result(self, status, message=""):
        """Log step result"""
        if status == "PASS":
            self.logger.info(f"✓ PASS: {message}")
        else:
            self.logger.error(f"✗ FAIL: {message}")

# Create singleton instance
logger = Logger()
