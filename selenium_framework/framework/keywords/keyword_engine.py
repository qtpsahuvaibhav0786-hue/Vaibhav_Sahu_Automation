"""
Keyword Engine Module.
Implements all test automation keywords using Selenium WebDriver.
"""

import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    NoAlertPresentException,
    ElementNotInteractableException
)

from framework.utils.logger import Logger


class KeywordEngine:
    """Executes test automation keywords using Selenium."""

    def __init__(self, driver_manager):
        """
        Initialize Keyword Engine.

        Args:
            driver_manager: SeleniumDriver instance
        """
        self.driver_manager = driver_manager
        self.driver = driver_manager.driver
        self.logger = Logger()

        # Map keywords to their implementation methods
        self.keyword_map = {
            # Navigation keywords
            "NAVIGATE": self._navigate,
            "REFRESH": self._refresh,
            "GO_BACK": self._go_back,
            "GO_FORWARD": self._go_forward,

            # Input keywords
            "ENTER": self._enter_text,
            "CLEAR": self._clear_text,
            "SELECT": self._select_dropdown,

            # Click keywords
            "CLICK": self._click,
            "DOUBLE_CLICK": self._double_click,
            "RIGHT_CLICK": self._right_click,

            # Verification keywords
            "VERIFY_TEXT": self._verify_text,
            "VERIFY_TITLE": self._verify_title,
            "VERIFY_URL": self._verify_url,
            "VERIFY_ELEMENT": self._verify_element,

            # Wait keywords
            "WAIT": self._wait,
            "WAIT_FOR_ELEMENT": self._wait_for_element,

            # Checkbox/Radio keywords
            "CHECK": self._check,
            "UNCHECK": self._uncheck,

            # Mouse interaction keywords
            "HOVER": self._hover,
            "SCROLL_TO": self._scroll_to,
            "DRAG_DROP": self._drag_drop,

            # Keyboard keywords
            "PRESS_KEY": self._press_key,

            # Frame keywords
            "SWITCH_TO_FRAME": self._switch_to_frame,
            "SWITCH_TO_DEFAULT": self._switch_to_default,

            # Alert keywords
            "ACCEPT_ALERT": self._accept_alert,
            "DISMISS_ALERT": self._dismiss_alert,
            "GET_ALERT_TEXT": self._get_alert_text,

            # Window/Tab keywords
            "CLOSE_TAB": self._close_tab,
            "SWITCH_WINDOW": self._switch_window,

            # Information retrieval keywords
            "GET_TEXT": self._get_text,
            "GET_ATTRIBUTE": self._get_attribute,
            "IS_VISIBLE": self._is_visible,
            "IS_ENABLED": self._is_enabled,
            "IS_SELECTED": self._is_selected,

            # JavaScript keywords
            "EXECUTE_SCRIPT": self._execute_script,
        }

    def execute_keyword(self, keyword, locator="", value=""):
        """
        Execute a keyword with given parameters.

        Args:
            keyword (str): Keyword to execute
            locator (str): Element locator
            value (str): Value/data for the keyword

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            keyword = keyword.strip().upper()

            if keyword not in self.keyword_map:
                return False, f"Unknown keyword: {keyword}"

            # Execute the keyword
            keyword_method = self.keyword_map[keyword]
            success, message = keyword_method(locator, value)

            return success, message

        except Exception as e:
            error_msg = f"Error executing keyword '{keyword}': {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg

    # Navigation Keywords

    def _navigate(self, locator, value):
        """Navigate to URL."""
        url = value if value else locator
        if not url:
            return False, "No URL provided"

        success = self.driver_manager.navigate_to(url)
        return success, f"Navigated to: {url}" if success else f"Failed to navigate to: {url}"

    def _refresh(self, locator, value):
        """Refresh the current page."""
        success = self.driver_manager.refresh_page()
        return success, "Page refreshed" if success else "Failed to refresh page"

    def _go_back(self, locator, value):
        """Navigate back."""
        success = self.driver_manager.go_back()
        return success, "Navigated back" if success else "Failed to navigate back"

    def _go_forward(self, locator, value):
        """Navigate forward."""
        success = self.driver_manager.go_forward()
        return success, "Navigated forward" if success else "Failed to navigate forward"

    # Input Keywords

    def _enter_text(self, locator, value):
        """Enter text into an element."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            element.clear()
            element.send_keys(value)
            return True, f"Entered text: {value}"
        except Exception as e:
            return False, f"Failed to enter text: {str(e)}"

    def _clear_text(self, locator, value):
        """Clear text from an element."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            element.clear()
            return True, "Text cleared"
        except Exception as e:
            return False, f"Failed to clear text: {str(e)}"

    def _select_dropdown(self, locator, value):
        """Select option from dropdown."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            select = Select(element)

            # Try to select by visible text first
            try:
                select.select_by_visible_text(value)
                return True, f"Selected option: {value}"
            except:
                pass

            # Try to select by value
            try:
                select.select_by_value(value)
                return True, f"Selected option by value: {value}"
            except:
                pass

            # Try to select by index
            try:
                select.select_by_index(int(value))
                return True, f"Selected option by index: {value}"
            except:
                pass

            return False, f"Could not select option: {value}"

        except Exception as e:
            return False, f"Failed to select dropdown: {str(e)}"

    # Click Keywords

    def _click(self, locator, value):
        """Click an element."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.wait_for_element(locator, condition="clickable")
        if not element:
            return False, f"Element not clickable: {locator}"

        try:
            element.click()
            return True, f"Clicked element"
        except Exception as e:
            # Try JavaScript click as fallback
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True, f"Clicked element (via JavaScript)"
            except:
                return False, f"Failed to click: {str(e)}"

    def _double_click(self, locator, value):
        """Double click an element."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            actions = self.driver_manager.get_action_chains()
            actions.double_click(element).perform()
            return True, f"Double clicked element"
        except Exception as e:
            return False, f"Failed to double click: {str(e)}"

    def _right_click(self, locator, value):
        """Right click an element."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            actions = self.driver_manager.get_action_chains()
            actions.context_click(element).perform()
            return True, f"Right clicked element"
        except Exception as e:
            return False, f"Failed to right click: {str(e)}"

    # Verification Keywords

    def _verify_text(self, locator, value):
        """Verify element contains expected text."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            element_text = element.text
            if value.lower() in element_text.lower():
                return True, f"Text verified: '{value}' found in '{element_text}'"
            else:
                return False, f"Text mismatch: Expected '{value}', Found '{element_text}'"
        except Exception as e:
            return False, f"Failed to verify text: {str(e)}"

    def _verify_title(self, locator, value):
        """Verify page title."""
        expected_title = value if value else locator
        try:
            actual_title = self.driver_manager.get_page_title()
            if expected_title.lower() in actual_title.lower():
                return True, f"Title verified: '{expected_title}'"
            else:
                return False, f"Title mismatch: Expected '{expected_title}', Found '{actual_title}'"
        except Exception as e:
            return False, f"Failed to verify title: {str(e)}"

    def _verify_url(self, locator, value):
        """Verify current URL."""
        expected_url = value if value else locator
        try:
            actual_url = self.driver_manager.get_current_url()
            if expected_url in actual_url:
                return True, f"URL verified: '{expected_url}'"
            else:
                return False, f"URL mismatch: Expected '{expected_url}', Found '{actual_url}'"
        except Exception as e:
            return False, f"Failed to verify URL: {str(e)}"

    def _verify_element(self, locator, value):
        """Verify element exists."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if element:
            return True, f"Element verified: {locator}"
        else:
            return False, f"Element not found: {locator}"

    # Wait Keywords

    def _wait(self, locator, value):
        """Wait for specified seconds."""
        try:
            wait_time = float(value) if value else 1
            time.sleep(wait_time)
            return True, f"Waited for {wait_time} seconds"
        except Exception as e:
            return False, f"Failed to wait: {str(e)}"

    def _wait_for_element(self, locator, value):
        """Wait for element to be visible."""
        if not locator:
            return False, "No locator provided"

        timeout = int(value) if value else None
        element = self.driver_manager.wait_for_element(locator, timeout=timeout, condition="visible")

        if element:
            return True, f"Element found: {locator}"
        else:
            return False, f"Element not found within timeout: {locator}"

    # Checkbox/Radio Keywords

    def _check(self, locator, value):
        """Check a checkbox or radio button."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            if not element.is_selected():
                element.click()
            return True, f"Checkbox/radio checked"
        except Exception as e:
            return False, f"Failed to check: {str(e)}"

    def _uncheck(self, locator, value):
        """Uncheck a checkbox."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            if element.is_selected():
                element.click()
            return True, f"Checkbox unchecked"
        except Exception as e:
            return False, f"Failed to uncheck: {str(e)}"

    # Mouse Interaction Keywords

    def _hover(self, locator, value):
        """Hover over an element."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            actions = self.driver_manager.get_action_chains()
            actions.move_to_element(element).perform()
            return True, f"Hovered over element"
        except Exception as e:
            return False, f"Failed to hover: {str(e)}"

    def _scroll_to(self, locator, value):
        """Scroll to an element."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Wait for scroll animation
            return True, f"Scrolled to element"
        except Exception as e:
            return False, f"Failed to scroll: {str(e)}"

    def _drag_drop(self, locator, value):
        """Drag and drop element."""
        if not locator or not value:
            return False, "Source and target locators required"

        source = self.driver_manager.get_element(locator)
        target = self.driver_manager.get_element(value)

        if not source or not target:
            return False, "Source or target element not found"

        try:
            actions = self.driver_manager.get_action_chains()
            actions.drag_and_drop(source, target).perform()
            return True, f"Drag and drop completed"
        except Exception as e:
            return False, f"Failed to drag and drop: {str(e)}"

    # Keyboard Keywords

    def _press_key(self, locator, value):
        """Press a keyboard key."""
        try:
            key_map = {
                "ENTER": Keys.ENTER,
                "TAB": Keys.TAB,
                "ESC": Keys.ESCAPE,
                "SPACE": Keys.SPACE,
                "BACKSPACE": Keys.BACKSPACE,
                "DELETE": Keys.DELETE,
                "ARROW_UP": Keys.ARROW_UP,
                "ARROW_DOWN": Keys.ARROW_DOWN,
                "ARROW_LEFT": Keys.ARROW_LEFT,
                "ARROW_RIGHT": Keys.ARROW_RIGHT,
            }

            key_to_press = key_map.get(value.upper(), value)

            if locator:
                element = self.driver_manager.get_element(locator)
                if not element:
                    return False, f"Element not found: {locator}"
                element.send_keys(key_to_press)
            else:
                # Press key on active element
                actions = self.driver_manager.get_action_chains()
                actions.send_keys(key_to_press).perform()

            return True, f"Pressed key: {value}"

        except Exception as e:
            return False, f"Failed to press key: {str(e)}"

    # Frame Keywords

    def _switch_to_frame(self, locator, value):
        """Switch to iframe."""
        frame_ref = value if value else locator
        success = self.driver_manager.switch_to_frame(frame_ref)
        return success, f"Switched to frame: {frame_ref}" if success else f"Failed to switch to frame"

    def _switch_to_default(self, locator, value):
        """Switch to default content."""
        success = self.driver_manager.switch_to_default_content()
        return success, "Switched to default content" if success else "Failed to switch to default content"

    # Alert Keywords

    def _accept_alert(self, locator, value):
        """Accept alert."""
        try:
            alert = Alert(self.driver)
            alert.accept()
            return True, "Alert accepted"
        except NoAlertPresentException:
            return False, "No alert present"
        except Exception as e:
            return False, f"Failed to accept alert: {str(e)}"

    def _dismiss_alert(self, locator, value):
        """Dismiss alert."""
        try:
            alert = Alert(self.driver)
            alert.dismiss()
            return True, "Alert dismissed"
        except NoAlertPresentException:
            return False, "No alert present"
        except Exception as e:
            return False, f"Failed to dismiss alert: {str(e)}"

    def _get_alert_text(self, locator, value):
        """Get alert text."""
        try:
            alert = Alert(self.driver)
            text = alert.text
            return True, f"Alert text: {text}"
        except NoAlertPresentException:
            return False, "No alert present"
        except Exception as e:
            return False, f"Failed to get alert text: {str(e)}"

    # Window/Tab Keywords

    def _close_tab(self, locator, value):
        """Close current tab."""
        try:
            self.driver.close()
            return True, "Tab closed"
        except Exception as e:
            return False, f"Failed to close tab: {str(e)}"

    def _switch_window(self, locator, value):
        """Switch to window by index or handle."""
        try:
            handles = self.driver.window_handles
            if value.isdigit():
                index = int(value)
                if 0 <= index < len(handles):
                    self.driver.switch_to.window(handles[index])
                    return True, f"Switched to window {index}"
                else:
                    return False, f"Invalid window index: {index}"
            else:
                self.driver.switch_to.window(value)
                return True, f"Switched to window: {value}"
        except Exception as e:
            return False, f"Failed to switch window: {str(e)}"

    # Information Retrieval Keywords

    def _get_text(self, locator, value):
        """Get element text."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            text = element.text
            return True, f"Element text: {text}"
        except Exception as e:
            return False, f"Failed to get text: {str(e)}"

    def _get_attribute(self, locator, value):
        """Get element attribute."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            attr_value = element.get_attribute(value)
            return True, f"Attribute '{value}': {attr_value}"
        except Exception as e:
            return False, f"Failed to get attribute: {str(e)}"

    def _is_visible(self, locator, value):
        """Check if element is visible."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            is_visible = element.is_displayed()
            return True, f"Element visible: {is_visible}"
        except Exception as e:
            return False, f"Failed to check visibility: {str(e)}"

    def _is_enabled(self, locator, value):
        """Check if element is enabled."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            is_enabled = element.is_enabled()
            return True, f"Element enabled: {is_enabled}"
        except Exception as e:
            return False, f"Failed to check if enabled: {str(e)}"

    def _is_selected(self, locator, value):
        """Check if element is selected."""
        if not locator:
            return False, "No locator provided"

        element = self.driver_manager.get_element(locator)
        if not element:
            return False, f"Element not found: {locator}"

        try:
            is_selected = element.is_selected()
            return True, f"Element selected: {is_selected}"
        except Exception as e:
            return False, f"Failed to check if selected: {str(e)}"

    # JavaScript Keywords

    def _execute_script(self, locator, value):
        """Execute JavaScript code."""
        try:
            script = value if value else locator
            result = self.driver.execute_script(script)
            return True, f"Script executed successfully: {result}"
        except Exception as e:
            return False, f"Failed to execute script: {str(e)}"
