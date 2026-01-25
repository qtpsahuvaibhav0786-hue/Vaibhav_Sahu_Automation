"""
Behave environment configuration
Contains hooks for test setup and teardown
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from selenium_behave_framework.utils.driver_factory import DriverFactory
from selenium_behave_framework.utils.logger import get_logger
from selenium_behave_framework.config.config import Config


def before_all(context):
    """
    Run before all tests
    Setup logging and global configuration
    """
    context.logger = get_logger()
    context.logger.info("=" * 60)
    context.logger.info("STARTING TEST EXECUTION")
    context.logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    context.logger.info("=" * 60)

    # Store configuration
    context.config.browser = os.getenv("SELENIUM_BROWSER", Config.BROWSER)
    context.config.headless = os.getenv("SELENIUM_HEADLESS", str(Config.HEADLESS)).lower() == "true"
    context.config.base_url = Config.BASE_URL

    # Create directories
    Config.create_directories()


def after_all(context):
    """
    Run after all tests
    Cleanup and final reporting
    """
    context.logger.info("=" * 60)
    context.logger.info("TEST EXECUTION COMPLETED")
    context.logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    context.logger.info("=" * 60)


def before_feature(context, feature):
    """
    Run before each feature
    """
    context.logger.info(f"\n{'='*60}")
    context.logger.info(f"FEATURE: {feature.name}")
    context.logger.info(f"{'='*60}")


def after_feature(context, feature):
    """
    Run after each feature
    """
    context.logger.info(f"Feature '{feature.name}' completed\n")


def before_scenario(context, scenario):
    """
    Run before each scenario
    Create new browser instance
    """
    context.logger.scenario_start(scenario.name)

    # Create new driver for each scenario
    context.driver = DriverFactory.create_driver(
        browser=context.config.browser,
        headless=context.config.headless
    )
    DriverFactory.set_driver(context.driver)

    context.logger.info(f"Browser: {context.config.browser}")


def after_scenario(context, scenario):
    """
    Run after each scenario
    Take screenshot on failure and close browser
    """
    status = "PASSED" if scenario.status == "passed" else "FAILED"

    # Take screenshot on failure
    if scenario.status == "failed" and hasattr(context, 'driver'):
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"{scenario.name.replace(' ', '_')}_{status}_{timestamp}"
            screenshot_path = Config.get_screenshot_path(screenshot_name)
            context.driver.save_screenshot(str(screenshot_path))
            context.logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            context.logger.error(f"Failed to capture screenshot: {str(e)}")

    # Close browser
    if hasattr(context, 'driver'):
        try:
            context.driver.quit()
        except Exception as e:
            context.logger.error(f"Failed to close browser: {str(e)}")

    DriverFactory.quit_driver()
    context.logger.scenario_end(scenario.name, status)


def before_step(context, step):
    """
    Run before each step
    """
    context.logger.step(f"{step.keyword} {step.name}")

    # Add slow mode delay if enabled
    if Config.SLOW_MODE:
        import time
        time.sleep(Config.SLOW_MODE_DELAY)


def after_step(context, step):
    """
    Run after each step
    Handle step failures
    """
    if step.status == "failed":
        context.logger.error(f"Step failed: {step.name}")
        if step.error_message:
            context.logger.error(f"Error: {step.error_message}")


def before_tag(context, tag):
    """
    Run before scenarios with specific tags
    """
    if tag == "skip":
        context.scenario.skip("Marked with @skip tag")


def after_tag(context, tag):
    """
    Run after scenarios with specific tags
    """
    pass
