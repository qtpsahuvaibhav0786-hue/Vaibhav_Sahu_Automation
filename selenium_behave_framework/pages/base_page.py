"""
Base Page Object class providing common functionality for all page objects
Implements the Page Object Model (POM) design pattern
"""

import time
from typing import Tuple, List, Optional, Any
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
    ElementNotInteractableException
)

from ..utils.wait_helper import WaitHelper
from ..utils.logger import get_logger
from ..config.config import Config


class BasePage:
    """
    Base Page Object class with common web element interactions
    All page objects should inherit from this class
    """

    def __init__(self, driver: WebDriver):
        """
        Initialize BasePage

        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WaitHelper(driver)
        self.logger = get_logger()
        self.actions = ActionChains(driver)

    # ==================== Navigation Methods ====================

    def navigate_to(self, url: str):
        """
        Navigate to a URL

        Args:
            url: URL to navigate to
        """
        self.logger.info(f"Navigating to: {url}")
        self.driver.get(url)

    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Get current page title"""
        return self.driver.title

    def refresh_page(self):
        """Refresh current page"""
        self.logger.info("Refreshing page")
        self.driver.refresh()

    def go_back(self):
        """Navigate back in browser history"""
        self.logger.info("Navigating back")
        self.driver.back()

    def go_forward(self):
        """Navigate forward in browser history"""
        self.logger.info("Navigating forward")
        self.driver.forward()

    # ==================== Element Finding Methods ====================

    def find_element(
        self,
        locator: Tuple[By, str],
        wait_for_visible: bool = True
    ) -> WebElement:
        """
        Find a single element

        Args:
            locator: Tuple of (By, locator_string)
            wait_for_visible: Wait for element to be visible

        Returns:
            WebElement
        """
        if wait_for_visible:
            return self.wait.wait_for_element_visible(locator)
        return self.driver.find_element(*locator)

    def find_elements(
        self,
        locator: Tuple[By, str],
        wait_for_presence: bool = True
    ) -> List[WebElement]:
        """
        Find multiple elements

        Args:
            locator: Tuple of (By, locator_string)
            wait_for_presence: Wait for elements to be present

        Returns:
            List of WebElements
        """
        if wait_for_presence:
            return self.wait.wait_for_elements_present(locator)
        return self.driver.find_elements(*locator)

    def is_element_visible(
        self,
        locator: Tuple[By, str],
        timeout: int = 5
    ) -> bool:
        """
        Check if element is visible

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Wait timeout

        Returns:
            True if visible
        """
        return self.wait.is_element_visible(locator, timeout)

    def is_element_present(
        self,
        locator: Tuple[By, str],
        timeout: int = 5
    ) -> bool:
        """
        Check if element is present in DOM

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Wait timeout

        Returns:
            True if present
        """
        return self.wait.is_element_present(locator, timeout)

    def is_element_enabled(self, locator: Tuple[By, str]) -> bool:
        """Check if element is enabled"""
        try:
            element = self.find_element(locator)
            return element.is_enabled()
        except (NoSuchElementException, TimeoutException):
            return False

    def is_element_selected(self, locator: Tuple[By, str]) -> bool:
        """Check if element is selected (for checkboxes/radio buttons)"""
        try:
            element = self.find_element(locator)
            return element.is_selected()
        except (NoSuchElementException, TimeoutException):
            return False

    # ==================== Click Methods ====================

    def click(self, locator: Tuple[By, str]):
        """
        Click an element

        Args:
            locator: Tuple of (By, locator_string)
        """
        self.logger.info(f"Clicking element: {locator}")
        element = self.wait.wait_for_element_clickable(locator)
        self._highlight_element(element)
        element.click()

    def double_click(self, locator: Tuple[By, str]):
        """
        Double-click an element

        Args:
            locator: Tuple of (By, locator_string)
        """
        self.logger.info(f"Double-clicking element: {locator}")
        element = self.wait.wait_for_element_clickable(locator)
        self._highlight_element(element)
        self.actions.double_click(element).perform()

    def right_click(self, locator: Tuple[By, str]):
        """
        Right-click an element

        Args:
            locator: Tuple of (By, locator_string)
        """
        self.logger.info(f"Right-clicking element: {locator}")
        element = self.wait.wait_for_element_clickable(locator)
        self._highlight_element(element)
        self.actions.context_click(element).perform()

    def click_with_js(self, locator: Tuple[By, str]):
        """
        Click element using JavaScript

        Args:
            locator: Tuple of (By, locator_string)
        """
        self.logger.info(f"JS clicking element: {locator}")
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    # ==================== Input Methods ====================

    def enter_text(
        self,
        locator: Tuple[By, str],
        text: str,
        clear_first: bool = True
    ):
        """
        Enter text into an input field

        Args:
            locator: Tuple of (By, locator_string)
            text: Text to enter
            clear_first: Clear field before entering text
        """
        self.logger.info(f"Entering text '{text}' into: {locator}")
        element = self.wait.wait_for_element_clickable(locator)
        self._highlight_element(element)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def clear_field(self, locator: Tuple[By, str]):
        """
        Clear an input field

        Args:
            locator: Tuple of (By, locator_string)
        """
        self.logger.info(f"Clearing field: {locator}")
        element = self.find_element(locator)
        element.clear()

    def press_key(self, locator: Tuple[By, str], key: str):
        """
        Press a keyboard key on element

        Args:
            locator: Tuple of (By, locator_string)
            key: Key to press (e.g., 'ENTER', 'TAB', 'ESCAPE')
        """
        self.logger.info(f"Pressing key '{key}' on: {locator}")
        element = self.find_element(locator)
        key_value = getattr(Keys, key.upper(), key)
        element.send_keys(key_value)

    def press_enter(self, locator: Tuple[By, str]):
        """Press Enter key on element"""
        self.press_key(locator, 'ENTER')

    def press_tab(self, locator: Tuple[By, str]):
        """Press Tab key on element"""
        self.press_key(locator, 'TAB')

    def press_escape(self, locator: Tuple[By, str]):
        """Press Escape key on element"""
        self.press_key(locator, 'ESCAPE')

    # ==================== Dropdown Methods ====================

    def select_by_value(self, locator: Tuple[By, str], value: str):
        """
        Select dropdown option by value

        Args:
            locator: Tuple of (By, locator_string)
            value: Option value to select
        """
        self.logger.info(f"Selecting value '{value}' from: {locator}")
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_value(value)

    def select_by_text(self, locator: Tuple[By, str], text: str):
        """
        Select dropdown option by visible text

        Args:
            locator: Tuple of (By, locator_string)
            text: Visible text to select
        """
        self.logger.info(f"Selecting text '{text}' from: {locator}")
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)

    def select_by_index(self, locator: Tuple[By, str], index: int):
        """
        Select dropdown option by index

        Args:
            locator: Tuple of (By, locator_string)
            index: Option index to select
        """
        self.logger.info(f"Selecting index '{index}' from: {locator}")
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_index(index)

    def get_selected_option(self, locator: Tuple[By, str]) -> str:
        """Get currently selected dropdown option text"""
        element = self.find_element(locator)
        select = Select(element)
        return select.first_selected_option.text

    def get_all_options(self, locator: Tuple[By, str]) -> List[str]:
        """Get all dropdown option texts"""
        element = self.find_element(locator)
        select = Select(element)
        return [option.text for option in select.options]

    # ==================== Checkbox/Radio Methods ====================

    def check_checkbox(self, locator: Tuple[By, str]):
        """
        Check a checkbox (only if not already checked)

        Args:
            locator: Tuple of (By, locator_string)
        """
        if not self.is_element_selected(locator):
            self.click(locator)
            self.logger.info(f"Checked checkbox: {locator}")
        else:
            self.logger.info(f"Checkbox already checked: {locator}")

    def uncheck_checkbox(self, locator: Tuple[By, str]):
        """
        Uncheck a checkbox (only if checked)

        Args:
            locator: Tuple of (By, locator_string)
        """
        if self.is_element_selected(locator):
            self.click(locator)
            self.logger.info(f"Unchecked checkbox: {locator}")
        else:
            self.logger.info(f"Checkbox already unchecked: {locator}")

    def select_radio_button(self, locator: Tuple[By, str]):
        """
        Select a radio button

        Args:
            locator: Tuple of (By, locator_string)
        """
        if not self.is_element_selected(locator):
            self.click(locator)
            self.logger.info(f"Selected radio button: {locator}")

    # ==================== Text/Attribute Methods ====================

    def get_text(self, locator: Tuple[By, str]) -> str:
        """
        Get element text

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            Element text
        """
        element = self.find_element(locator)
        return element.text

    def get_attribute(self, locator: Tuple[By, str], attribute: str) -> str:
        """
        Get element attribute value

        Args:
            locator: Tuple of (By, locator_string)
            attribute: Attribute name

        Returns:
            Attribute value
        """
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    def get_value(self, locator: Tuple[By, str]) -> str:
        """Get input field value"""
        return self.get_attribute(locator, "value")

    def get_css_property(self, locator: Tuple[By, str], property_name: str) -> str:
        """Get CSS property value"""
        element = self.find_element(locator)
        return element.value_of_css_property(property_name)

    # ==================== Hover/Scroll Methods ====================

    def hover(self, locator: Tuple[By, str]):
        """
        Hover over an element

        Args:
            locator: Tuple of (By, locator_string)
        """
        self.logger.info(f"Hovering over: {locator}")
        element = self.find_element(locator)
        self.actions.move_to_element(element).perform()

    def scroll_to_element(self, locator: Tuple[By, str]):
        """
        Scroll element into view

        Args:
            locator: Tuple of (By, locator_string)
        """
        self.logger.info(f"Scrolling to element: {locator}")
        element = self.find_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )

    def scroll_to_top(self):
        """Scroll to top of page"""
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_by(self, x: int, y: int):
        """Scroll by pixel amount"""
        self.driver.execute_script(f"window.scrollBy({x}, {y});")

    # ==================== Frame/Window Methods ====================

    def switch_to_frame(self, frame_reference):
        """
        Switch to iframe

        Args:
            frame_reference: Frame name, id, index, or WebElement
        """
        self.logger.info(f"Switching to frame: {frame_reference}")
        self.driver.switch_to.frame(frame_reference)

    def switch_to_default_content(self):
        """Switch back to default content from frame"""
        self.logger.info("Switching to default content")
        self.driver.switch_to.default_content()

    def switch_to_parent_frame(self):
        """Switch to parent frame"""
        self.driver.switch_to.parent_frame()

    def switch_to_window(self, window_handle: str):
        """Switch to window by handle"""
        self.logger.info(f"Switching to window: {window_handle}")
        self.driver.switch_to.window(window_handle)

    def switch_to_new_window(self):
        """Switch to newly opened window"""
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])

    def get_window_handles(self) -> List[str]:
        """Get all window handles"""
        return self.driver.window_handles

    def get_current_window_handle(self) -> str:
        """Get current window handle"""
        return self.driver.current_window_handle

    def close_current_window(self):
        """Close current window"""
        self.driver.close()

    # ==================== Alert Methods ====================

    def accept_alert(self):
        """Accept alert dialog"""
        self.logger.info("Accepting alert")
        alert = self.wait.wait_for_alert()
        alert.accept()

    def dismiss_alert(self):
        """Dismiss alert dialog"""
        self.logger.info("Dismissing alert")
        alert = self.wait.wait_for_alert()
        alert.dismiss()

    def get_alert_text(self) -> str:
        """Get alert text"""
        alert = self.wait.wait_for_alert()
        return alert.text

    def enter_text_in_alert(self, text: str):
        """Enter text in alert prompt"""
        alert = self.wait.wait_for_alert()
        alert.send_keys(text)

    # ==================== Screenshot Methods ====================

    def take_screenshot(self, name: str) -> str:
        """
        Take screenshot and save to file

        Args:
            name: Screenshot name

        Returns:
            Screenshot file path
        """
        screenshot_path = Config.get_screenshot_path(name)
        self.driver.save_screenshot(str(screenshot_path))
        self.logger.info(f"Screenshot saved: {screenshot_path}")
        return str(screenshot_path)

    def take_element_screenshot(
        self,
        locator: Tuple[By, str],
        name: str
    ) -> str:
        """
        Take screenshot of specific element

        Args:
            locator: Tuple of (By, locator_string)
            name: Screenshot name

        Returns:
            Screenshot file path
        """
        element = self.find_element(locator)
        screenshot_path = Config.get_screenshot_path(name)
        element.screenshot(str(screenshot_path))
        self.logger.info(f"Element screenshot saved: {screenshot_path}")
        return str(screenshot_path)

    # ==================== JavaScript Methods ====================

    def execute_script(self, script: str, *args) -> Any:
        """
        Execute JavaScript

        Args:
            script: JavaScript code
            *args: Script arguments

        Returns:
            Script return value
        """
        return self.driver.execute_script(script, *args)

    def execute_async_script(self, script: str, *args) -> Any:
        """
        Execute asynchronous JavaScript

        Args:
            script: JavaScript code
            *args: Script arguments

        Returns:
            Script return value
        """
        return self.driver.execute_async_script(script, *args)

    # ==================== Wait Methods ====================

    def wait_for_page_load(self, timeout: int = None):
        """Wait for page to fully load"""
        timeout = timeout or Config.PAGE_LOAD_TIMEOUT
        self.wait.wait_for_condition(
            lambda d: d.execute_script("return document.readyState") == "complete",
            timeout
        )

    def wait_for_ajax(self, timeout: int = None):
        """Wait for all AJAX calls to complete"""
        timeout = timeout or Config.EXPLICIT_WAIT
        self.wait.wait_for_condition(
            lambda d: d.execute_script("return jQuery.active == 0"),
            timeout
        )

    def explicit_wait(self, seconds: float):
        """
        Explicit wait (use sparingly)

        Args:
            seconds: Seconds to wait
        """
        time.sleep(seconds)

    # ==================== Verification Methods ====================

    def verify_text(
        self,
        locator: Tuple[By, str],
        expected_text: str,
        exact_match: bool = True
    ) -> bool:
        """
        Verify element contains expected text

        Args:
            locator: Tuple of (By, locator_string)
            expected_text: Expected text
            exact_match: Require exact match

        Returns:
            True if text matches
        """
        actual_text = self.get_text(locator)
        if exact_match:
            return actual_text == expected_text
        return expected_text in actual_text

    def verify_title(self, expected_title: str) -> bool:
        """Verify page title"""
        return self.get_page_title() == expected_title

    def verify_url(self, expected_url: str, contains: bool = False) -> bool:
        """Verify current URL"""
        current_url = self.get_current_url()
        if contains:
            return expected_url in current_url
        return current_url == expected_url

    # ==================== Utility Methods ====================

    def _highlight_element(self, element: WebElement, duration: float = 0.2):
        """
        Highlight element briefly (for debugging)

        Args:
            element: WebElement to highlight
            duration: Highlight duration in seconds
        """
        if Config.SLOW_MODE:
            original_style = element.get_attribute("style")
            self.driver.execute_script(
                "arguments[0].style.border='3px solid red';",
                element
            )
            time.sleep(duration)
            self.driver.execute_script(
                f"arguments[0].style.cssText='{original_style}';",
                element
            )

    @staticmethod
    def get_locator(locator_type: str, locator_value: str) -> Tuple[By, str]:
        """
        Convert locator type string to By tuple

        Args:
            locator_type: Type of locator (id, name, xpath, css, etc.)
            locator_value: Locator value

        Returns:
            Tuple of (By, locator_value)
        """
        locator_map = {
            'id': By.ID,
            'name': By.NAME,
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'class': By.CLASS_NAME,
            'class_name': By.CLASS_NAME,
            'tag': By.TAG_NAME,
            'tag_name': By.TAG_NAME,
            'link': By.LINK_TEXT,
            'link_text': By.LINK_TEXT,
            'partial_link': By.PARTIAL_LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT
        }
        by = locator_map.get(locator_type.lower(), By.XPATH)
        return (by, locator_value)
