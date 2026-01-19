"""
Browser Manager module for Playwright browser operations
"""
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from framework.config.config import BROWSER_CONFIG, SCREENSHOTS_DIR
from framework.utils.logger import logger
from datetime import datetime
from pathlib import Path

class BrowserManager:
    """Manages Playwright browser lifecycle and operations"""

    def __init__(self):
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None

    def start_browser(self):
        """Start Playwright browser"""
        try:
            self.playwright = sync_playwright().start()

            browser_type = BROWSER_CONFIG["browser"].lower()

            if browser_type == "firefox":
                self.browser = self.playwright.firefox.launch(
                    headless=BROWSER_CONFIG["headless"],
                    slow_mo=BROWSER_CONFIG["slow_mo"]
                )
            elif browser_type == "webkit":
                self.browser = self.playwright.webkit.launch(
                    headless=BROWSER_CONFIG["headless"],
                    slow_mo=BROWSER_CONFIG["slow_mo"]
                )
            else:  # chromium (default)
                self.browser = self.playwright.chromium.launch(
                    headless=BROWSER_CONFIG["headless"],
                    slow_mo=BROWSER_CONFIG["slow_mo"]
                )

            self.context = self.browser.new_context(
                viewport=BROWSER_CONFIG["viewport"],
                accept_downloads=True,
                record_video_dir=None
            )

            # Set default timeout
            self.context.set_default_timeout(BROWSER_CONFIG["timeout"])

            self.page = self.context.new_page()

            logger.info(f"Browser started: {browser_type.upper()}")
            logger.info(f"Headless mode: {BROWSER_CONFIG['headless']}")

            return True

        except Exception as e:
            logger.error(f"Error starting browser: {str(e)}")
            return False

    def close_browser(self):
        """Close browser and cleanup"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()

            logger.info("Browser closed successfully")

        except Exception as e:
            logger.error(f"Error closing browser: {str(e)}")

    def navigate_to(self, url):
        """Navigate to URL"""
        try:
            self.page.goto(url, wait_until="domcontentloaded")
            logger.info(f"Navigated to: {url}")
            return True
        except Exception as e:
            logger.error(f"Error navigating to {url}: {str(e)}")
            return False

    def get_element(self, locator):
        """Get element by locator"""
        try:
            return self.page.locator(locator)
        except Exception as e:
            logger.error(f"Error locating element '{locator}': {str(e)}")
            return None

    def take_screenshot(self, name="screenshot"):
        """Take screenshot and save to screenshots directory"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = Path(SCREENSHOTS_DIR) / filename

            self.page.screenshot(path=str(filepath), full_page=True)
            logger.info(f"Screenshot saved: {filepath}")

            return str(filepath)
        except Exception as e:
            logger.error(f"Error taking screenshot: {str(e)}")
            return None

    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be visible"""
        try:
            timeout = timeout or BROWSER_CONFIG["timeout"]
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=timeout)
            return True
        except Exception as e:
            logger.error(f"Element not found or timeout: {locator}")
            return False

    def get_page_title(self):
        """Get current page title"""
        try:
            return self.page.title()
        except Exception as e:
            logger.error(f"Error getting page title: {str(e)}")
            return None

    def get_current_url(self):
        """Get current page URL"""
        try:
            return self.page.url
        except Exception as e:
            logger.error(f"Error getting current URL: {str(e)}")
            return None
