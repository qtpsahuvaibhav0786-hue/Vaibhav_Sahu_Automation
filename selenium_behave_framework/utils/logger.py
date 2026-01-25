"""
Logger utility for the Selenium Behave Framework
Provides colored console output and file logging
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

try:
    import colorlog
    COLORLOG_AVAILABLE = True
except ImportError:
    COLORLOG_AVAILABLE = False


class Logger:
    """
    Singleton Logger class providing colored console and file logging
    """

    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None

    # Color configuration for different log levels
    LOG_COLORS = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        name: str = "SeleniumBehaveFramework",
        level: str = "INFO",
        log_dir: Optional[Path] = None,
        log_to_file: bool = True,
        log_to_console: bool = True
    ):
        if self._logger is not None:
            return

        self._logger = logging.getLogger(name)
        self._logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        self._logger.handlers = []  # Clear existing handlers

        # Console handler with colors
        if log_to_console:
            console_handler = self._create_console_handler()
            self._logger.addHandler(console_handler)

        # File handler
        if log_to_file and log_dir:
            file_handler = self._create_file_handler(log_dir)
            self._logger.addHandler(file_handler)

    def _create_console_handler(self) -> logging.Handler:
        """Create a colored console handler"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        if COLORLOG_AVAILABLE:
            formatter = colorlog.ColoredFormatter(
                '%(log_color)s%(asctime)s | %(levelname)-8s | %(message)s%(reset)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors=self.LOG_COLORS
            )
        else:
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        console_handler.setFormatter(formatter)
        return console_handler

    def _create_file_handler(self, log_dir: Path) -> logging.Handler:
        """Create a file handler for logging to file"""
        log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f"test_execution_{timestamp}.log"

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        return file_handler

    @property
    def logger(self) -> logging.Logger:
        """Get the underlying logger instance"""
        return self._logger

    def debug(self, message: str):
        """Log debug message"""
        self._logger.debug(message)

    def info(self, message: str):
        """Log info message"""
        self._logger.info(message)

    def warning(self, message: str):
        """Log warning message"""
        self._logger.warning(message)

    def error(self, message: str):
        """Log error message"""
        self._logger.error(message)

    def critical(self, message: str):
        """Log critical message"""
        self._logger.critical(message)

    def step(self, message: str):
        """Log a test step (info level with step prefix)"""
        self._logger.info(f"[STEP] {message}")

    def test_start(self, test_name: str):
        """Log test start"""
        self._logger.info(f"{'='*60}")
        self._logger.info(f"[TEST START] {test_name}")
        self._logger.info(f"{'='*60}")

    def test_end(self, test_name: str, status: str):
        """Log test end with status"""
        self._logger.info(f"{'='*60}")
        self._logger.info(f"[TEST END] {test_name} - Status: {status}")
        self._logger.info(f"{'='*60}")

    def scenario_start(self, scenario_name: str):
        """Log scenario start"""
        self._logger.info(f"[SCENARIO START] {scenario_name}")

    def scenario_end(self, scenario_name: str, status: str):
        """Log scenario end with status"""
        self._logger.info(f"[SCENARIO END] {scenario_name} - Status: {status}")

    def keyword(self, keyword: str, element: str = "", value: str = ""):
        """Log keyword execution"""
        msg = f"[KEYWORD] {keyword}"
        if element:
            msg += f" | Element: {element}"
        if value:
            msg += f" | Value: {value}"
        self._logger.info(msg)


# Create a default logger instance
def get_logger(
    name: str = "SeleniumBehaveFramework",
    level: str = "INFO",
    log_dir: Optional[Path] = None
) -> Logger:
    """Get or create a logger instance"""
    from ..config.config import Config
    if log_dir is None:
        log_dir = Config.LOGS_DIR
    return Logger(name=name, level=level, log_dir=log_dir)
