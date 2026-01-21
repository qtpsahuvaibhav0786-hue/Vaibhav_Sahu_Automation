"""
Selenium WebDriver Manager Module.
Handles browser lifecycle, navigation, element interactions, and screenshots.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException
)
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
import datetime
from pathlib import Path

from framework.config.config import Config
from framework.utils.logger import Logger


class SeleniumDriver:
    """Manages Selenium WebDriver instance and browser operations."""

    def __init__(self):
        """Initialize Selenium Driver."""
        self.driver = None
        self.wait = None
        self.actions = None
        self.logger = Logger()

    def start_browser(self):
        """
        Initialize and start the browser based on configuration.

        Returns:
            bool: True if browser started successfully, False otherwise
        """
        try:
            browser = Config.BROWSER.lower()
            self.logger.info(f"Starting {browser} browser (Headless: {Config.HEADLESS})")

            if browser == "chrome":
                options = webdriver.ChromeOptions()
                for option in Config.CHROME_OPTIONS:
                    options.add_argument(option)
                if Config.HEADLESS:
                    options.add_argument("--headless")
                if not Config.MAXIMIZE_WINDOW:
                    options.add_argument(f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}")

                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)

            elif browser == "firefox":
                options = webdriver.FirefoxOptions()
                for option in Config.FIREFOX_OPTIONS:
                    options.add_argument(option)
                if Config.HEADLESS:
                    options.add_argument("--headless")

                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)

            elif browser == "edge":
                options = webdriver.EdgeOptions()
                for option in Config.EDGE_OPTIONS:
                    options.add_argument(option)
                if Config.HEADLESS:
                    options.add_argument("--headless")

                service = EdgeService(EdgeChromiumDriverManager().install())
                self.driver = webdriver.Edge(service=service, options=options)

            else:
                self.logger.error(f"Unsupported browser: {browser}")
                return False

            # Configure timeouts
            self.driver.implicitly_wait(Config.IMPLICIT_WAIT)
            self.driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
            self.driver.set_script_timeout(Config.SCRIPT_TIMEOUT)

            # Maximize window if configured
            if Config.MAXIMIZE_WINDOW:
                self.driver.maximize_window()
            else:
                self.driver.set_window_size(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

            # Initialize WebDriverWait and ActionChains
            self.wait = WebDriverWait(self.driver, Config.DEFAULT_WAIT)
            self.actions = ActionChains(self.driver)

            self.logger.success("Browser started successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start browser: {str(e)}")
            return False

    def close_browser(self):
        """Close the browser and cleanup resources."""
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("Browser closed successfully")
        except Exception as e:
            self.logger.warning(f"Error closing browser: {str(e)}")

    def navigate_to(self, url):
        """
        Navigate to a URL.

        Args:
            url (str): The URL to navigate to

        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            self.logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            self.logger.success(f"Successfully navigated to: {url}")
            return True
        except Exception as e:
            self.logger.error(f"Navigation failed: {str(e)}")
            return False

    def get_element(self, locator, timeout=None):
        """
        Find and return a web element using various locator strategies.

        Args:
            locator (str): Element locator (xpath, id, css, etc.)
            timeout (int): Optional timeout in seconds

        Returns:
            WebElement: The found element or None
        """
        try:
            wait_time = timeout if timeout else Config.DEFAULT_WAIT
            wait = WebDriverWait(self.driver, wait_time)

            # Determine locator strategy
            by_type, locator_value = self._parse_locator(locator)

            # Wait for element to be present
            element = wait.until(EC.presence_of_element_located((by_type, locator_value)))
            return element

        except TimeoutException:
            self.logger.warning(f"Element not found within {wait_time} seconds: {locator}")
            return None
        except Exception as e:
            self.logger.error(f"Error finding element '{locator}': {str(e)}")
            return None

    def _parse_locator(self, locator):
        """
        Parse locator string to determine locator strategy.

        Args:
            locator (str): Locator string

        Returns:
            tuple: (By type, locator value)
        """
        locator = locator.strip()

        # XPath
        if locator.startswith("//") or locator.startswith("(//"):
            return By.XPATH, locator

        # ID
        elif locator.startswith("id="):
            return By.ID, locator[3:]

        # CSS Selector
        elif locator.startswith("css="):
            return By.CSS_SELECTOR, locator[4:]

        # Name
        elif locator.startswith("name="):
            return By.NAME, locator[5:]

        # Class Name
        elif locator.startswith("class="):
            return By.CLASS_NAME, locator[6:]

        # Link Text
        elif locator.startswith("link="):
            return By.LINK_TEXT, locator[5:]

        # Partial Link Text
        elif locator.startswith("partial_link="):
            return By.PARTIAL_LINK_TEXT, locator[13:]

        # Tag Name
        elif locator.startswith("tag="):
            return By.TAG_NAME, locator[4:]

        # Default to XPath if contains / or (
        elif "/" in locator or locator.startswith("("):
            return By.XPATH, locator

        # Default to ID
        else:
            return By.ID, locator

    def wait_for_element(self, locator, timeout=None, condition="visible"):
        """
        Wait for element with specific condition.

        Args:
            locator (str): Element locator
            timeout (int): Wait timeout in seconds
            condition (str): Wait condition (visible, clickable, present)

        Returns:
            WebElement: The found element or None
        """
        try:
            wait_time = timeout if timeout else Config.DEFAULT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            by_type, locator_value = self._parse_locator(locator)

            if condition == "visible":
                element = wait.until(EC.visibility_of_element_located((by_type, locator_value)))
            elif condition == "clickable":
                element = wait.until(EC.element_to_be_clickable((by_type, locator_value)))
            elif condition == "present":
                element = wait.until(EC.presence_of_element_located((by_type, locator_value)))
            else:
                element = wait.until(EC.presence_of_element_located((by_type, locator_value)))

            return element

        except TimeoutException:
            self.logger.warning(f"Element not {condition} within {wait_time} seconds: {locator}")
            return None
        except Exception as e:
            self.logger.error(f"Error waiting for element: {str(e)}")
            return None

    def take_screenshot(self, name):
        """
        Capture screenshot and save to configured directory.

        Args:
            name (str): Screenshot filename (without extension)

        Returns:
            str: Path to saved screenshot or None
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = Config.get_screenshot_path(filename)

            self.driver.save_screenshot(str(filepath))
            self.logger.info(f"Screenshot saved: {filename}")
            return str(filepath)

        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            return None

    def get_page_title(self):
        """
        Get current page title.

        Returns:
            str: Page title
        """
        try:
            return self.driver.title
        except Exception as e:
            self.logger.error(f"Failed to get page title: {str(e)}")
            return ""

    def get_current_url(self):
        """
        Get current page URL.

        Returns:
            str: Current URL
        """
        try:
            return self.driver.current_url
        except Exception as e:
            self.logger.error(f"Failed to get current URL: {str(e)}")
            return ""

    def execute_script(self, script, *args):
        """
        Execute JavaScript in the browser.

        Args:
            script (str): JavaScript code to execute
            *args: Arguments to pass to the script

        Returns:
            Any: Script execution result
        """
        try:
            return self.driver.execute_script(script, *args)
        except Exception as e:
            self.logger.error(f"Failed to execute script: {str(e)}")
            return None

    def switch_to_frame(self, frame_reference):
        """
        Switch to an iframe.

        Args:
            frame_reference: Frame index, name, or WebElement

        Returns:
            bool: True if switch successful, False otherwise
        """
        try:
            if isinstance(frame_reference, str):
                # Try to find frame by name or id
                element = self.get_element(frame_reference)
                if element:
                    self.driver.switch_to.frame(element)
                else:
                    self.driver.switch_to.frame(frame_reference)
            else:
                self.driver.switch_to.frame(frame_reference)

            self.logger.info(f"Switched to frame: {frame_reference}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to switch to frame: {str(e)}")
            return False

    def switch_to_default_content(self):
        """
        Switch back to default content from iframe.

        Returns:
            bool: True if switch successful, False otherwise
        """
        try:
            self.driver.switch_to.default_content()
            self.logger.info("Switched to default content")
            return True
        except Exception as e:
            self.logger.error(f"Failed to switch to default content: {str(e)}")
            return False

    def get_action_chains(self):
        """
        Get ActionChains instance for complex interactions.

        Returns:
            ActionChains: ActionChains instance
        """
        return ActionChains(self.driver)

    def refresh_page(self):
        """Refresh the current page."""
        try:
            self.driver.refresh()
            self.logger.info("Page refreshed")
            return True
        except Exception as e:
            self.logger.error(f"Failed to refresh page: {str(e)}")
            return False

    def go_back(self):
        """Navigate back in browser history."""
        try:
            self.driver.back()
            self.logger.info("Navigated back")
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate back: {str(e)}")
            return False

    def go_forward(self):
        """Navigate forward in browser history."""
        try:
            self.driver.forward()
            self.logger.info("Navigated forward")
            return True
        except Exception as e:
            self.logger.error(f"Failed to navigate forward: {str(e)}")
            return False
