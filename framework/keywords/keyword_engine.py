"""
Keyword Engine module - Executes keywords defined in test data
"""
import time
from framework.core.browser_manager import BrowserManager
from framework.utils.logger import logger

class KeywordEngine:
    """
    Keyword Engine to execute various keywords on web elements
    Supported Keywords:
    - NAVIGATE: Navigate to URL
    - CLICK: Click on element
    - ENTER: Enter text in input field
    - SELECT: Select option from dropdown
    - VERIFY_TEXT: Verify text content
    - VERIFY_TITLE: Verify page title
    - VERIFY_URL: Verify current URL
    - WAIT: Wait for specified seconds
    - CLEAR: Clear input field
    - CHECK: Check checkbox
    - UNCHECK: Uncheck checkbox
    - HOVER: Hover over element
    - DOUBLE_CLICK: Double click element
    - RIGHT_CLICK: Right click element
    - PRESS_KEY: Press keyboard key
    - GET_TEXT: Get element text
    - IS_VISIBLE: Check if element is visible
    - IS_ENABLED: Check if element is enabled
    - SCROLL_TO: Scroll to element
    - SWITCH_TO_FRAME: Switch to iframe
    - SWITCH_TO_DEFAULT: Switch to default content
    - ACCEPT_ALERT: Accept alert dialog
    - DISMISS_ALERT: Dismiss alert dialog
    - REFRESH: Refresh page
    - GO_BACK: Navigate back
    - GO_FORWARD: Navigate forward
    - CLOSE_TAB: Close current tab
    """

    def __init__(self, browser_manager: BrowserManager):
        self.browser = browser_manager
        self.page = browser_manager.page

    def execute_keyword(self, keyword, locator, value=""):
        """
        Execute keyword based on keyword name
        Returns: (success: bool, message: str)
        """
        try:
            keyword = keyword.upper().strip()
            logger.keyword_execution(keyword, locator, value)

            # Map keywords to methods
            keyword_map = {
                "NAVIGATE": self.navigate,
                "CLICK": self.click,
                "ENTER": self.enter_text,
                "SELECT": self.select_option,
                "VERIFY_TEXT": self.verify_text,
                "VERIFY_TITLE": self.verify_title,
                "VERIFY_URL": self.verify_url,
                "WAIT": self.wait,
                "CLEAR": self.clear,
                "CHECK": self.check,
                "UNCHECK": self.uncheck,
                "HOVER": self.hover,
                "DOUBLE_CLICK": self.double_click,
                "RIGHT_CLICK": self.right_click,
                "PRESS_KEY": self.press_key,
                "GET_TEXT": self.get_text,
                "IS_VISIBLE": self.is_visible,
                "IS_ENABLED": self.is_enabled,
                "SCROLL_TO": self.scroll_to,
                "SWITCH_TO_FRAME": self.switch_to_frame,
                "SWITCH_TO_DEFAULT": self.switch_to_default,
                "ACCEPT_ALERT": self.accept_alert,
                "DISMISS_ALERT": self.dismiss_alert,
                "REFRESH": self.refresh,
                "GO_BACK": self.go_back,
                "GO_FORWARD": self.go_forward,
                "CLOSE_TAB": self.close_tab,
                "WAIT_FOR_ELEMENT": self.wait_for_element
            }

            if keyword in keyword_map:
                result = keyword_map[keyword](locator, value)
                return result
            else:
                error_msg = f"Keyword '{keyword}' is not supported"
                logger.error(error_msg)
                return False, error_msg

        except Exception as e:
            error_msg = f"Error executing keyword '{keyword}': {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    # Keyword Methods

    def navigate(self, url, value=""):
        """Navigate to URL"""
        try:
            self.page.goto(url, wait_until="domcontentloaded")
            return True, f"Successfully navigated to {url}"
        except Exception as e:
            return False, f"Failed to navigate: {str(e)}"

    def click(self, locator, value=""):
        """Click element"""
        try:
            element = self.page.locator(locator)
            element.click(timeout=10000)
            return True, f"Clicked on element: {locator}"
        except Exception as e:
            return False, f"Failed to click: {str(e)}"

    def enter_text(self, locator, value):
        """Enter text in input field"""
        try:
            element = self.page.locator(locator)
            element.fill(value, timeout=10000)
            return True, f"Entered text '{value}' in {locator}"
        except Exception as e:
            return False, f"Failed to enter text: {str(e)}"

    def select_option(self, locator, value):
        """Select option from dropdown"""
        try:
            element = self.page.locator(locator)
            element.select_option(value, timeout=10000)
            return True, f"Selected option '{value}' from {locator}"
        except Exception as e:
            return False, f"Failed to select option: {str(e)}"

    def verify_text(self, locator, expected_text):
        """Verify element text"""
        try:
            element = self.page.locator(locator)
            actual_text = element.text_content(timeout=10000)
            if expected_text in actual_text:
                return True, f"Text verification passed: '{expected_text}' found in '{actual_text}'"
            else:
                return False, f"Text verification failed: Expected '{expected_text}', but found '{actual_text}'"
        except Exception as e:
            return False, f"Failed to verify text: {str(e)}"

    def verify_title(self, expected_title, value=""):
        """Verify page title"""
        try:
            actual_title = self.page.title()
            if expected_title in actual_title:
                return True, f"Title verification passed: '{expected_title}' found in '{actual_title}'"
            else:
                return False, f"Title verification failed: Expected '{expected_title}', but found '{actual_title}'"
        except Exception as e:
            return False, f"Failed to verify title: {str(e)}"

    def verify_url(self, expected_url, value=""):
        """Verify current URL"""
        try:
            actual_url = self.page.url
            if expected_url in actual_url:
                return True, f"URL verification passed: '{expected_url}' found in '{actual_url}'"
            else:
                return False, f"URL verification failed: Expected '{expected_url}', but found '{actual_url}'"
        except Exception as e:
            return False, f"Failed to verify URL: {str(e)}"

    def wait(self, seconds, value=""):
        """Wait for specified seconds"""
        try:
            wait_time = float(seconds) if seconds else 1
            time.sleep(wait_time)
            return True, f"Waited for {wait_time} seconds"
        except Exception as e:
            return False, f"Failed to wait: {str(e)}"

    def clear(self, locator, value=""):
        """Clear input field"""
        try:
            element = self.page.locator(locator)
            element.clear(timeout=10000)
            return True, f"Cleared input field: {locator}"
        except Exception as e:
            return False, f"Failed to clear: {str(e)}"

    def check(self, locator, value=""):
        """Check checkbox"""
        try:
            element = self.page.locator(locator)
            element.check(timeout=10000)
            return True, f"Checked checkbox: {locator}"
        except Exception as e:
            return False, f"Failed to check: {str(e)}"

    def uncheck(self, locator, value=""):
        """Uncheck checkbox"""
        try:
            element = self.page.locator(locator)
            element.uncheck(timeout=10000)
            return True, f"Unchecked checkbox: {locator}"
        except Exception as e:
            return False, f"Failed to uncheck: {str(e)}"

    def hover(self, locator, value=""):
        """Hover over element"""
        try:
            element = self.page.locator(locator)
            element.hover(timeout=10000)
            return True, f"Hovered over element: {locator}"
        except Exception as e:
            return False, f"Failed to hover: {str(e)}"

    def double_click(self, locator, value=""):
        """Double click element"""
        try:
            element = self.page.locator(locator)
            element.dblclick(timeout=10000)
            return True, f"Double clicked on element: {locator}"
        except Exception as e:
            return False, f"Failed to double click: {str(e)}"

    def right_click(self, locator, value=""):
        """Right click element"""
        try:
            element = self.page.locator(locator)
            element.click(button="right", timeout=10000)
            return True, f"Right clicked on element: {locator}"
        except Exception as e:
            return False, f"Failed to right click: {str(e)}"

    def press_key(self, key, value=""):
        """Press keyboard key"""
        try:
            self.page.keyboard.press(key)
            return True, f"Pressed key: {key}"
        except Exception as e:
            return False, f"Failed to press key: {str(e)}"

    def get_text(self, locator, value=""):
        """Get element text"""
        try:
            element = self.page.locator(locator)
            text = element.text_content(timeout=10000)
            return True, f"Retrieved text: {text}"
        except Exception as e:
            return False, f"Failed to get text: {str(e)}"

    def is_visible(self, locator, value=""):
        """Check if element is visible"""
        try:
            element = self.page.locator(locator)
            visible = element.is_visible(timeout=10000)
            return True, f"Element visibility: {visible}"
        except Exception as e:
            return False, f"Failed to check visibility: {str(e)}"

    def is_enabled(self, locator, value=""):
        """Check if element is enabled"""
        try:
            element = self.page.locator(locator)
            enabled = element.is_enabled(timeout=10000)
            return True, f"Element enabled state: {enabled}"
        except Exception as e:
            return False, f"Failed to check enabled state: {str(e)}"

    def scroll_to(self, locator, value=""):
        """Scroll to element"""
        try:
            element = self.page.locator(locator)
            element.scroll_into_view_if_needed(timeout=10000)
            return True, f"Scrolled to element: {locator}"
        except Exception as e:
            return False, f"Failed to scroll: {str(e)}"

    def switch_to_frame(self, locator, value=""):
        """Switch to iframe"""
        try:
            frame = self.page.frame_locator(locator)
            return True, f"Switched to frame: {locator}"
        except Exception as e:
            return False, f"Failed to switch frame: {str(e)}"

    def switch_to_default(self, locator="", value=""):
        """Switch to default content"""
        try:
            self.page.main_frame()
            return True, "Switched to default content"
        except Exception as e:
            return False, f"Failed to switch to default: {str(e)}"

    def accept_alert(self, locator="", value=""):
        """Accept alert dialog"""
        try:
            self.page.on("dialog", lambda dialog: dialog.accept())
            return True, "Alert accepted"
        except Exception as e:
            return False, f"Failed to accept alert: {str(e)}"

    def dismiss_alert(self, locator="", value=""):
        """Dismiss alert dialog"""
        try:
            self.page.on("dialog", lambda dialog: dialog.dismiss())
            return True, "Alert dismissed"
        except Exception as e:
            return False, f"Failed to dismiss alert: {str(e)}"

    def refresh(self, locator="", value=""):
        """Refresh page"""
        try:
            self.page.reload()
            return True, "Page refreshed"
        except Exception as e:
            return False, f"Failed to refresh: {str(e)}"

    def go_back(self, locator="", value=""):
        """Navigate back"""
        try:
            self.page.go_back()
            return True, "Navigated back"
        except Exception as e:
            return False, f"Failed to go back: {str(e)}"

    def go_forward(self, locator="", value=""):
        """Navigate forward"""
        try:
            self.page.go_forward()
            return True, "Navigated forward"
        except Exception as e:
            return False, f"Failed to go forward: {str(e)}"

    def close_tab(self, locator="", value=""):
        """Close current tab"""
        try:
            self.page.close()
            return True, "Tab closed"
        except Exception as e:
            return False, f"Failed to close tab: {str(e)}"

    def wait_for_element(self, locator, value=""):
        """Wait for element to be visible"""
        try:
            timeout = int(value) * 1000 if value else 10000
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=timeout)
            return True, f"Element found: {locator}"
        except Exception as e:
            return False, f"Element not found: {str(e)}"
