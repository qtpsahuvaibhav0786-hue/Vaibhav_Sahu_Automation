"""
Keyword Engine for Selenium-based keyword-driven testing
Provides a comprehensive set of keywords for web automation
"""

import time
from typing import Optional, Dict, Any, Callable
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException
)

from ..utils.logger import get_logger
from ..config.config import Config


class KeywordEngine:
    """
    Keyword Engine providing 40+ keywords for web automation
    Supports navigation, input, verification, and advanced interactions
    """

    def __init__(self, driver: WebDriver):
        """
        Initialize Keyword Engine

        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.logger = get_logger()
        self.timeout = Config.EXPLICIT_WAIT
        self.variables: Dict[str, Any] = {}

        # Register all keywords
        self._keywords: Dict[str, Callable] = {
            # Navigation keywords
            'NAVIGATE': self.navigate,
            'OPEN': self.navigate,
            'OPEN_URL': self.navigate,
            'REFRESH': self.refresh,
            'GO_BACK': self.go_back,
            'GO_FORWARD': self.go_forward,
            'MAXIMIZE': self.maximize_window,
            'RESIZE': self.resize_window,

            # Input keywords
            'ENTER': self.enter_text,
            'TYPE': self.enter_text,
            'INPUT': self.enter_text,
            'CLEAR': self.clear_field,
            'CLEAR_AND_ENTER': self.clear_and_enter,

            # Click keywords
            'CLICK': self.click,
            'DOUBLE_CLICK': self.double_click,
            'RIGHT_CLICK': self.right_click,
            'JS_CLICK': self.js_click,
            'CLICK_IF_EXISTS': self.click_if_exists,

            # Dropdown keywords
            'SELECT': self.select_dropdown,
            'SELECT_BY_VALUE': self.select_by_value,
            'SELECT_BY_TEXT': self.select_by_text,
            'SELECT_BY_INDEX': self.select_by_index,

            # Checkbox/Radio keywords
            'CHECK': self.check_checkbox,
            'UNCHECK': self.uncheck_checkbox,
            'SELECT_RADIO': self.select_radio,

            # Verification keywords
            'VERIFY_TEXT': self.verify_text,
            'VERIFY_TITLE': self.verify_title,
            'VERIFY_URL': self.verify_url,
            'VERIFY_ELEMENT_PRESENT': self.verify_element_present,
            'VERIFY_ELEMENT_VISIBLE': self.verify_element_visible,
            'VERIFY_ELEMENT_NOT_VISIBLE': self.verify_element_not_visible,
            'VERIFY_ELEMENT_ENABLED': self.verify_element_enabled,
            'VERIFY_ELEMENT_DISABLED': self.verify_element_disabled,
            'VERIFY_ATTRIBUTE': self.verify_attribute,
            'VERIFY_VALUE': self.verify_value,

            # Wait keywords
            'WAIT': self.wait,
            'WAIT_FOR_ELEMENT': self.wait_for_element,
            'WAIT_FOR_VISIBLE': self.wait_for_visible,
            'WAIT_FOR_CLICKABLE': self.wait_for_clickable,
            'WAIT_FOR_TEXT': self.wait_for_text,
            'WAIT_FOR_PAGE_LOAD': self.wait_for_page_load,

            # Keyboard keywords
            'PRESS_KEY': self.press_key,
            'PRESS_ENTER': self.press_enter,
            'PRESS_TAB': self.press_tab,
            'PRESS_ESCAPE': self.press_escape,

            # Mouse keywords
            'HOVER': self.hover,
            'DRAG_AND_DROP': self.drag_and_drop,
            'SCROLL_TO': self.scroll_to_element,
            'SCROLL_BY': self.scroll_by,
            'SCROLL_TO_TOP': self.scroll_to_top,
            'SCROLL_TO_BOTTOM': self.scroll_to_bottom,

            # Frame/Window keywords
            'SWITCH_TO_FRAME': self.switch_to_frame,
            'SWITCH_TO_DEFAULT': self.switch_to_default,
            'SWITCH_TO_WINDOW': self.switch_to_window,
            'SWITCH_TO_NEW_WINDOW': self.switch_to_new_window,
            'CLOSE_WINDOW': self.close_window,

            # Alert keywords
            'ACCEPT_ALERT': self.accept_alert,
            'DISMISS_ALERT': self.dismiss_alert,
            'GET_ALERT_TEXT': self.get_alert_text,
            'ENTER_ALERT_TEXT': self.enter_alert_text,

            # Data keywords
            'GET_TEXT': self.get_text,
            'GET_ATTRIBUTE': self.get_attribute,
            'GET_VALUE': self.get_value,
            'STORE_TEXT': self.store_text,
            'STORE_ATTRIBUTE': self.store_attribute,
            'STORE_VALUE': self.store_value,

            # Screenshot keywords
            'SCREENSHOT': self.take_screenshot,
            'ELEMENT_SCREENSHOT': self.element_screenshot,

            # JavaScript keywords
            'EXECUTE_JS': self.execute_js,
            'SET_VALUE_JS': self.set_value_js,

            # Assertion keywords
            'ASSERT_TRUE': self.assert_true,
            'ASSERT_FALSE': self.assert_false,
            'ASSERT_EQUALS': self.assert_equals,
            'ASSERT_CONTAINS': self.assert_contains,

            # Utility keywords
            'PRINT': self.print_message,
            'LOG': self.log_message,
            'PAUSE': self.pause,
        }

    def execute(
        self,
        keyword: str,
        locator_type: str = None,
        locator_value: str = None,
        data: str = None
    ) -> Any:
        """
        Execute a keyword with given parameters

        Args:
            keyword: Keyword name to execute
            locator_type: Type of locator (id, xpath, css, etc.)
            locator_value: Locator value
            data: Additional data/value for the keyword

        Returns:
            Result of keyword execution
        """
        keyword = keyword.upper().strip()

        if keyword not in self._keywords:
            raise ValueError(f"Unknown keyword: {keyword}")

        self.logger.keyword(keyword, locator_value or "", data or "")

        try:
            func = self._keywords[keyword]

            # Prepare locator if provided
            locator = None
            if locator_type and locator_value:
                locator = self._get_locator(locator_type, locator_value)

            # Execute keyword based on its signature
            if locator and data:
                return func(locator, data)
            elif locator:
                return func(locator)
            elif data:
                return func(data)
            else:
                return func()

        except Exception as e:
            self.logger.error(f"Keyword '{keyword}' failed: {str(e)}")
            raise

    def _get_locator(self, locator_type: str, locator_value: str) -> tuple:
        """Convert locator type string to By tuple"""
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

    def _find_element(self, locator: tuple, timeout: int = None) -> WebElement:
        """Find element with wait"""
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def _find_clickable(self, locator: tuple, timeout: int = None) -> WebElement:
        """Find clickable element"""
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def _find_visible(self, locator: tuple, timeout: int = None) -> WebElement:
        """Find visible element"""
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    # ==================== Navigation Keywords ====================

    def navigate(self, url: str) -> None:
        """Navigate to URL"""
        self.driver.get(url)
        self.logger.info(f"Navigated to: {url}")

    def refresh(self) -> None:
        """Refresh current page"""
        self.driver.refresh()

    def go_back(self) -> None:
        """Navigate back"""
        self.driver.back()

    def go_forward(self) -> None:
        """Navigate forward"""
        self.driver.forward()

    def maximize_window(self) -> None:
        """Maximize browser window"""
        self.driver.maximize_window()

    def resize_window(self, size: str) -> None:
        """Resize window (format: 'widthxheight')"""
        width, height = map(int, size.lower().split('x'))
        self.driver.set_window_size(width, height)

    # ==================== Input Keywords ====================

    def enter_text(self, locator: tuple, text: str) -> None:
        """Enter text into element"""
        element = self._find_clickable(locator)
        element.clear()
        element.send_keys(text)

    def clear_field(self, locator: tuple) -> None:
        """Clear input field"""
        element = self._find_element(locator)
        element.clear()

    def clear_and_enter(self, locator: tuple, text: str) -> None:
        """Clear field and enter text"""
        element = self._find_clickable(locator)
        element.clear()
        element.send_keys(text)

    # ==================== Click Keywords ====================

    def click(self, locator: tuple) -> None:
        """Click element"""
        element = self._find_clickable(locator)
        element.click()

    def double_click(self, locator: tuple) -> None:
        """Double-click element"""
        element = self._find_clickable(locator)
        ActionChains(self.driver).double_click(element).perform()

    def right_click(self, locator: tuple) -> None:
        """Right-click element"""
        element = self._find_clickable(locator)
        ActionChains(self.driver).context_click(element).perform()

    def js_click(self, locator: tuple) -> None:
        """Click element using JavaScript"""
        element = self._find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def click_if_exists(self, locator: tuple) -> bool:
        """Click element if it exists"""
        try:
            element = self._find_clickable(locator, timeout=3)
            element.click()
            return True
        except TimeoutException:
            return False

    # ==================== Dropdown Keywords ====================

    def select_dropdown(self, locator: tuple, value: str) -> None:
        """Select dropdown by visible text"""
        element = self._find_element(locator)
        Select(element).select_by_visible_text(value)

    def select_by_value(self, locator: tuple, value: str) -> None:
        """Select dropdown by value"""
        element = self._find_element(locator)
        Select(element).select_by_value(value)

    def select_by_text(self, locator: tuple, text: str) -> None:
        """Select dropdown by visible text"""
        element = self._find_element(locator)
        Select(element).select_by_visible_text(text)

    def select_by_index(self, locator: tuple, index: str) -> None:
        """Select dropdown by index"""
        element = self._find_element(locator)
        Select(element).select_by_index(int(index))

    # ==================== Checkbox/Radio Keywords ====================

    def check_checkbox(self, locator: tuple) -> None:
        """Check checkbox if not already checked"""
        element = self._find_element(locator)
        if not element.is_selected():
            element.click()

    def uncheck_checkbox(self, locator: tuple) -> None:
        """Uncheck checkbox if checked"""
        element = self._find_element(locator)
        if element.is_selected():
            element.click()

    def select_radio(self, locator: tuple) -> None:
        """Select radio button"""
        element = self._find_element(locator)
        if not element.is_selected():
            element.click()

    # ==================== Verification Keywords ====================

    def verify_text(self, locator: tuple, expected_text: str) -> bool:
        """Verify element text"""
        element = self._find_visible(locator)
        actual_text = element.text
        matches = expected_text in actual_text
        self.logger.info(f"Verify text: expected='{expected_text}', actual='{actual_text}', matches={matches}")
        return matches

    def verify_title(self, expected_title: str) -> bool:
        """Verify page title"""
        actual_title = self.driver.title
        matches = expected_title in actual_title
        self.logger.info(f"Verify title: expected='{expected_title}', actual='{actual_title}'")
        return matches

    def verify_url(self, expected_url: str) -> bool:
        """Verify current URL"""
        actual_url = self.driver.current_url
        matches = expected_url in actual_url
        self.logger.info(f"Verify URL: expected='{expected_url}', actual='{actual_url}'")
        return matches

    def verify_element_present(self, locator: tuple) -> bool:
        """Verify element is present in DOM"""
        try:
            self._find_element(locator, timeout=5)
            return True
        except TimeoutException:
            return False

    def verify_element_visible(self, locator: tuple) -> bool:
        """Verify element is visible"""
        try:
            self._find_visible(locator, timeout=5)
            return True
        except TimeoutException:
            return False

    def verify_element_not_visible(self, locator: tuple) -> bool:
        """Verify element is not visible"""
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def verify_element_enabled(self, locator: tuple) -> bool:
        """Verify element is enabled"""
        element = self._find_element(locator)
        return element.is_enabled()

    def verify_element_disabled(self, locator: tuple) -> bool:
        """Verify element is disabled"""
        element = self._find_element(locator)
        return not element.is_enabled()

    def verify_attribute(self, locator: tuple, attr_value: str) -> bool:
        """Verify element attribute (format: 'attr_name=expected_value')"""
        attr_name, expected_value = attr_value.split('=', 1)
        element = self._find_element(locator)
        actual_value = element.get_attribute(attr_name)
        return actual_value == expected_value

    def verify_value(self, locator: tuple, expected_value: str) -> bool:
        """Verify input value"""
        element = self._find_element(locator)
        actual_value = element.get_attribute('value')
        return actual_value == expected_value

    # ==================== Wait Keywords ====================

    def wait(self, seconds: str) -> None:
        """Wait for specified seconds"""
        time.sleep(float(seconds))

    def wait_for_element(self, locator: tuple, timeout: str = None) -> WebElement:
        """Wait for element to be present"""
        t = int(timeout) if timeout else self.timeout
        return self._find_element(locator, t)

    def wait_for_visible(self, locator: tuple, timeout: str = None) -> WebElement:
        """Wait for element to be visible"""
        t = int(timeout) if timeout else self.timeout
        return self._find_visible(locator, t)

    def wait_for_clickable(self, locator: tuple, timeout: str = None) -> WebElement:
        """Wait for element to be clickable"""
        t = int(timeout) if timeout else self.timeout
        return self._find_clickable(locator, t)

    def wait_for_text(self, locator: tuple, text: str) -> bool:
        """Wait for element to contain text"""
        wait = WebDriverWait(self.driver, self.timeout)
        return wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_for_page_load(self) -> None:
        """Wait for page to fully load"""
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    # ==================== Keyboard Keywords ====================

    def press_key(self, locator: tuple, key: str) -> None:
        """Press keyboard key on element"""
        element = self._find_element(locator)
        key_value = getattr(Keys, key.upper(), key)
        element.send_keys(key_value)

    def press_enter(self, locator: tuple = None) -> None:
        """Press Enter key"""
        if locator:
            element = self._find_element(locator)
            element.send_keys(Keys.ENTER)
        else:
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()

    def press_tab(self, locator: tuple = None) -> None:
        """Press Tab key"""
        if locator:
            element = self._find_element(locator)
            element.send_keys(Keys.TAB)
        else:
            ActionChains(self.driver).send_keys(Keys.TAB).perform()

    def press_escape(self, locator: tuple = None) -> None:
        """Press Escape key"""
        if locator:
            element = self._find_element(locator)
            element.send_keys(Keys.ESCAPE)
        else:
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    # ==================== Mouse Keywords ====================

    def hover(self, locator: tuple) -> None:
        """Hover over element"""
        element = self._find_visible(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def drag_and_drop(self, source_locator: tuple, target: str) -> None:
        """Drag and drop (target is locator value)"""
        source = self._find_element(source_locator)
        target_locator = (By.XPATH, target)
        target_element = self._find_element(target_locator)
        ActionChains(self.driver).drag_and_drop(source, target_element).perform()

    def scroll_to_element(self, locator: tuple) -> None:
        """Scroll element into view"""
        element = self._find_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )

    def scroll_by(self, pixels: str) -> None:
        """Scroll by pixels (format: 'x,y')"""
        x, y = map(int, pixels.split(','))
        self.driver.execute_script(f"window.scrollBy({x}, {y});")

    def scroll_to_top(self) -> None:
        """Scroll to top of page"""
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # ==================== Frame/Window Keywords ====================

    def switch_to_frame(self, frame_ref: str) -> None:
        """Switch to frame by name, id, or index"""
        try:
            # Try as index first
            self.driver.switch_to.frame(int(frame_ref))
        except ValueError:
            # Try as name/id
            self.driver.switch_to.frame(frame_ref)

    def switch_to_default(self) -> None:
        """Switch to default content"""
        self.driver.switch_to.default_content()

    def switch_to_window(self, window_handle: str) -> None:
        """Switch to window by handle"""
        self.driver.switch_to.window(window_handle)

    def switch_to_new_window(self) -> None:
        """Switch to newly opened window"""
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])

    def close_window(self) -> None:
        """Close current window"""
        self.driver.close()

    # ==================== Alert Keywords ====================

    def accept_alert(self) -> None:
        """Accept alert"""
        WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self) -> None:
        """Dismiss alert"""
        WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.dismiss()

    def get_alert_text(self) -> str:
        """Get alert text"""
        WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        return self.driver.switch_to.alert.text

    def enter_alert_text(self, text: str) -> None:
        """Enter text in alert prompt"""
        WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.send_keys(text)

    # ==================== Data Keywords ====================

    def get_text(self, locator: tuple) -> str:
        """Get element text"""
        element = self._find_visible(locator)
        return element.text

    def get_attribute(self, locator: tuple, attr_name: str) -> str:
        """Get element attribute"""
        element = self._find_element(locator)
        return element.get_attribute(attr_name)

    def get_value(self, locator: tuple) -> str:
        """Get input value"""
        element = self._find_element(locator)
        return element.get_attribute('value')

    def store_text(self, locator: tuple, variable_name: str) -> None:
        """Store element text in variable"""
        text = self.get_text(locator)
        self.variables[variable_name] = text

    def store_attribute(self, locator: tuple, params: str) -> None:
        """Store attribute value (format: 'attr_name,var_name')"""
        attr_name, var_name = params.split(',')
        value = self.get_attribute(locator, attr_name)
        self.variables[var_name] = value

    def store_value(self, locator: tuple, variable_name: str) -> None:
        """Store input value in variable"""
        value = self.get_value(locator)
        self.variables[variable_name] = value

    # ==================== Screenshot Keywords ====================

    def take_screenshot(self, name: str = None) -> str:
        """Take screenshot"""
        from datetime import datetime
        if not name:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        path = Config.get_screenshot_path(name)
        self.driver.save_screenshot(str(path))
        self.logger.info(f"Screenshot saved: {path}")
        return str(path)

    def element_screenshot(self, locator: tuple, name: str = None) -> str:
        """Take element screenshot"""
        from datetime import datetime
        if not name:
            name = f"element_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        element = self._find_visible(locator)
        path = Config.get_screenshot_path(name)
        element.screenshot(str(path))
        return str(path)

    # ==================== JavaScript Keywords ====================

    def execute_js(self, script: str) -> Any:
        """Execute JavaScript"""
        return self.driver.execute_script(script)

    def set_value_js(self, locator: tuple, value: str) -> None:
        """Set value using JavaScript"""
        element = self._find_element(locator)
        self.driver.execute_script(f"arguments[0].value = '{value}';", element)

    # ==================== Assertion Keywords ====================

    def assert_true(self, condition: str) -> None:
        """Assert condition is true"""
        # Evaluate simple conditions
        result = eval(condition, {"variables": self.variables})
        assert result, f"Assertion failed: {condition}"

    def assert_false(self, condition: str) -> None:
        """Assert condition is false"""
        result = eval(condition, {"variables": self.variables})
        assert not result, f"Assertion failed: {condition}"

    def assert_equals(self, params: str) -> None:
        """Assert two values are equal (format: 'value1,value2')"""
        value1, value2 = params.split(',', 1)
        assert value1 == value2, f"Assertion failed: '{value1}' != '{value2}'"

    def assert_contains(self, params: str) -> None:
        """Assert value contains substring (format: 'text,substring')"""
        text, substring = params.split(',', 1)
        assert substring in text, f"Assertion failed: '{text}' does not contain '{substring}'"

    # ==================== Utility Keywords ====================

    def print_message(self, message: str) -> None:
        """Print message to console"""
        print(message)

    def log_message(self, message: str) -> None:
        """Log message"""
        self.logger.info(message)

    def pause(self, seconds: str = "5") -> None:
        """Pause execution"""
        time.sleep(float(seconds))

    def get_variable(self, name: str) -> Any:
        """Get stored variable value"""
        return self.variables.get(name)

    def set_variable(self, name: str, value: Any) -> None:
        """Set variable value"""
        self.variables[name] = value

    def list_keywords(self) -> list:
        """Get list of all available keywords"""
        return list(self._keywords.keys())
