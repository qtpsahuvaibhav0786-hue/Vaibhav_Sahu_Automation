"""
WebDriver Factory for creating and managing browser instances
Supports Chrome, Firefox, Edge with WebDriver Manager
"""

from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.remote.webdriver import WebDriver

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False

from ..config.config import Config


class DriverFactory:
    """
    Factory class for creating WebDriver instances
    Supports Chrome, Firefox, and Edge browsers
    """

    _driver: Optional[WebDriver] = None

    @classmethod
    def create_driver(
        cls,
        browser: str = None,
        headless: bool = None,
        remote: bool = None
    ) -> WebDriver:
        """
        Create and return a WebDriver instance

        Args:
            browser: Browser type (chrome, firefox, edge)
            headless: Run browser in headless mode
            remote: Use remote WebDriver (Selenium Grid)

        Returns:
            WebDriver instance
        """
        browser = browser or Config.BROWSER
        headless = headless if headless is not None else Config.HEADLESS
        remote = remote if remote is not None else Config.REMOTE_EXECUTION

        browser = browser.lower()

        if remote:
            return cls._create_remote_driver(browser, headless)

        if browser == "chrome":
            return cls._create_chrome_driver(headless)
        elif browser == "firefox":
            return cls._create_firefox_driver(headless)
        elif browser == "edge":
            return cls._create_edge_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

    @classmethod
    def _create_chrome_driver(cls, headless: bool) -> WebDriver:
        """Create Chrome WebDriver instance"""
        options = ChromeOptions()

        if headless:
            options.add_argument("--headless=new")

        # Common Chrome options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.add_argument(f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}")

        # Disable automation flags
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        if Config.CHROME_DRIVER_PATH:
            service = ChromeService(executable_path=Config.CHROME_DRIVER_PATH)
        elif WEBDRIVER_MANAGER_AVAILABLE:
            service = ChromeService(ChromeDriverManager().install())
        else:
            service = ChromeService()

        driver = webdriver.Chrome(service=service, options=options)
        cls._configure_driver(driver)
        return driver

    @classmethod
    def _create_firefox_driver(cls, headless: bool) -> WebDriver:
        """Create Firefox WebDriver instance"""
        options = FirefoxOptions()

        if headless:
            options.add_argument("--headless")

        options.add_argument(f"--width={Config.WINDOW_WIDTH}")
        options.add_argument(f"--height={Config.WINDOW_HEIGHT}")

        if Config.FIREFOX_DRIVER_PATH:
            service = FirefoxService(executable_path=Config.FIREFOX_DRIVER_PATH)
        elif WEBDRIVER_MANAGER_AVAILABLE:
            service = FirefoxService(GeckoDriverManager().install())
        else:
            service = FirefoxService()

        driver = webdriver.Firefox(service=service, options=options)
        cls._configure_driver(driver)
        return driver

    @classmethod
    def _create_edge_driver(cls, headless: bool) -> WebDriver:
        """Create Edge WebDriver instance"""
        options = EdgeOptions()

        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}")

        if Config.EDGE_DRIVER_PATH:
            service = EdgeService(executable_path=Config.EDGE_DRIVER_PATH)
        elif WEBDRIVER_MANAGER_AVAILABLE:
            service = EdgeService(EdgeChromiumDriverManager().install())
        else:
            service = EdgeService()

        driver = webdriver.Edge(service=service, options=options)
        cls._configure_driver(driver)
        return driver

    @classmethod
    def _create_remote_driver(cls, browser: str, headless: bool) -> WebDriver:
        """Create Remote WebDriver instance for Selenium Grid"""
        capabilities = {
            "browserName": browser,
            "platformName": "ANY"
        }

        if browser == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
        elif browser == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
        elif browser == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
        else:
            raise ValueError(f"Unsupported browser for remote: {browser}")

        driver = webdriver.Remote(
            command_executor=Config.SELENIUM_GRID_URL,
            options=options
        )
        cls._configure_driver(driver)
        return driver

    @classmethod
    def _configure_driver(cls, driver: WebDriver):
        """Configure common driver settings"""
        driver.implicitly_wait(Config.IMPLICIT_WAIT)
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

        if Config.MAXIMIZE_WINDOW:
            driver.maximize_window()
        else:
            driver.set_window_size(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

    @classmethod
    def get_driver(cls) -> Optional[WebDriver]:
        """Get the current driver instance"""
        return cls._driver

    @classmethod
    def set_driver(cls, driver: WebDriver):
        """Set the current driver instance"""
        cls._driver = driver

    @classmethod
    def quit_driver(cls):
        """Quit and cleanup the driver"""
        if cls._driver:
            try:
                cls._driver.quit()
            except Exception:
                pass
            finally:
                cls._driver = None
