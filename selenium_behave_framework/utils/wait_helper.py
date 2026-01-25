"""
Wait Helper utility for Selenium WebDriver
Provides various wait conditions and utilities
"""

from typing import Tuple, List, Optional, Callable
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from ..config.config import Config


class WaitHelper:
    """
    Helper class for implementing various wait strategies
    """

    def __init__(self, driver: WebDriver, timeout: int = None):
        """
        Initialize WaitHelper

        Args:
            driver: WebDriver instance
            timeout: Default timeout in seconds
        """
        self.driver = driver
        self.timeout = timeout or Config.EXPLICIT_WAIT

    def wait_for_element_visible(
        self,
        locator: Tuple[By, str],
        timeout: int = None
    ) -> WebElement:
        """
        Wait for element to be visible

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Wait timeout in seconds

        Returns:
            WebElement when visible

        Raises:
            TimeoutException: If element not visible within timeout
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(
        self,
        locator: Tuple[By, str],
        timeout: int = None
    ) -> WebElement:
        """
        Wait for element to be clickable

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Wait timeout in seconds

        Returns:
            WebElement when clickable
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_for_element_present(
        self,
        locator: Tuple[By, str],
        timeout: int = None
    ) -> WebElement:
        """
        Wait for element to be present in DOM

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Wait timeout in seconds

        Returns:
            WebElement when present
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def wait_for_elements_present(
        self,
        locator: Tuple[By, str],
        timeout: int = None
    ) -> List[WebElement]:
        """
        Wait for multiple elements to be present

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Wait timeout in seconds

        Returns:
            List of WebElements
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def wait_for_element_invisible(
        self,
        locator: Tuple[By, str],
        timeout: int = None
    ) -> bool:
        """
        Wait for element to become invisible

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Wait timeout in seconds

        Returns:
            True if element is invisible
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_text_in_element(
        self,
        locator: Tuple[By, str],
        text: str,
        timeout: int = None
    ) -> bool:
        """
        Wait for specific text to appear in element

        Args:
            locator: Tuple of (By, locator_string)
            text: Expected text
            timeout: Wait timeout in seconds

        Returns:
            True if text found
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_for_title_contains(
        self,
        title: str,
        timeout: int = None
    ) -> bool:
        """
        Wait for page title to contain text

        Args:
            title: Expected title text
            timeout: Wait timeout in seconds

        Returns:
            True if title contains text
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.title_contains(title))

    def wait_for_url_contains(
        self,
        url_part: str,
        timeout: int = None
    ) -> bool:
        """
        Wait for URL to contain text

        Args:
            url_part: Expected URL part
            timeout: Wait timeout in seconds

        Returns:
            True if URL contains text
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.url_contains(url_part))

    def wait_for_alert(self, timeout: int = None):
        """
        Wait for alert to be present

        Args:
            timeout: Wait timeout in seconds

        Returns:
            Alert object
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.alert_is_present())

    def wait_for_frame(
        self,
        frame_locator,
        timeout: int = None
    ) -> bool:
        """
        Wait for frame to be available and switch to it

        Args:
            frame_locator: Frame locator (name, id, index, or WebElement)
            timeout: Wait timeout in seconds

        Returns:
            True if switched to frame
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.frame_to_be_available_and_switch_to_it(frame_locator))

    def wait_for_staleness(
        self,
        element: WebElement,
        timeout: int = None
    ) -> bool:
        """
        Wait for element to become stale

        Args:
            element: WebElement to watch
            timeout: Wait timeout in seconds

        Returns:
            True if element is stale
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.staleness_of(element))

    def wait_for_condition(
        self,
        condition: Callable,
        timeout: int = None,
        poll_frequency: float = 0.5
    ):
        """
        Wait for custom condition

        Args:
            condition: Callable that returns truthy value when condition met
            timeout: Wait timeout in seconds
            poll_frequency: How often to check condition

        Returns:
            Result of condition function
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=poll_frequency,
            ignored_exceptions=[StaleElementReferenceException]
        )
        return wait.until(condition)

    def is_element_visible(
        self,
        locator: Tuple[By, str],
        timeout: int = 5
    ) -> bool:
        """
        Check if element is visible (non-blocking)

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Wait timeout in seconds

        Returns:
            True if visible, False otherwise
        """
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_present(
        self,
        locator: Tuple[By, str],
        timeout: int = 5
    ) -> bool:
        """
        Check if element is present in DOM (non-blocking)

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Wait timeout in seconds

        Returns:
            True if present, False otherwise
        """
        try:
            self.wait_for_element_present(locator, timeout)
            return True
        except TimeoutException:
            return False
