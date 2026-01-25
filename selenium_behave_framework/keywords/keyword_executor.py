"""
Keyword Executor for running keyword-driven tests from Excel or other data sources
"""

import time
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from .keyword_engine import KeywordEngine
from ..utils.driver_factory import DriverFactory
from ..utils.excel_reader import ExcelReader
from ..utils.logger import get_logger
from ..config.config import Config


class TestResult:
    """Class to hold test execution results"""

    def __init__(self, test_case_id: str, description: str = ""):
        self.test_case_id = test_case_id
        self.description = description
        self.status = "Not Started"
        self.steps: List[Dict[str, Any]] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.error_message: Optional[str] = None
        self.screenshot_path: Optional[str] = None

    @property
    def duration(self) -> float:
        """Get test duration in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0

    def add_step(self, step_no: int, keyword: str, status: str, message: str = ""):
        """Add step result"""
        self.steps.append({
            "step_no": step_no,
            "keyword": keyword,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "test_case_id": self.test_case_id,
            "description": self.description,
            "status": self.status,
            "duration": self.duration,
            "steps": self.steps,
            "error_message": self.error_message,
            "screenshot_path": self.screenshot_path
        }


class KeywordExecutor:
    """
    Executes keyword-driven tests from Excel data source
    Manages test lifecycle and reporting
    """

    def __init__(
        self,
        test_data_path: Path = None,
        browser: str = None,
        headless: bool = None
    ):
        """
        Initialize Keyword Executor

        Args:
            test_data_path: Path to Excel test data file
            browser: Browser type to use
            headless: Run in headless mode
        """
        self.test_data_path = test_data_path or Config.get_test_data_path()
        self.browser = browser or Config.BROWSER
        self.headless = headless if headless is not None else Config.HEADLESS
        self.logger = get_logger()
        self.results: List[TestResult] = []
        self.driver: Optional[WebDriver] = None
        self.keyword_engine: Optional[KeywordEngine] = None

    def run_all_tests(self) -> List[TestResult]:
        """
        Run all tests from test data file

        Returns:
            List of test results
        """
        self.logger.info("=" * 60)
        self.logger.info("STARTING KEYWORD-DRIVEN TEST EXECUTION")
        self.logger.info(f"Test Data: {self.test_data_path}")
        self.logger.info("=" * 60)

        start_time = datetime.now()

        try:
            with ExcelReader(self.test_data_path) as reader:
                # Get test scenarios from Master sheet
                scenarios = reader.get_test_scenarios()

                self.logger.info(f"Found {len(scenarios)} test scenarios to execute")

                for scenario in scenarios:
                    test_case_id = scenario['test_case_id']
                    screen_flow = scenario.get('screen_flow', '')
                    description = scenario.get('description', '')

                    self.logger.info(f"\n{'='*40}")
                    self.logger.info(f"Executing: {test_case_id}")
                    self.logger.info(f"{'='*40}")

                    result = self._run_test_case(
                        reader,
                        test_case_id,
                        screen_flow,
                        description
                    )
                    self.results.append(result)

        except Exception as e:
            self.logger.error(f"Test execution failed: {str(e)}")
            raise

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        self._print_summary(duration)
        return self.results

    def run_test_case(
        self,
        test_case_id: str,
        keywords: List[Dict[str, Any]]
    ) -> TestResult:
        """
        Run a single test case with provided keywords

        Args:
            test_case_id: Test case identifier
            keywords: List of keyword steps

        Returns:
            Test result
        """
        result = TestResult(test_case_id)
        result.start_time = datetime.now()
        result.status = "Running"

        try:
            # Create browser
            self._setup_driver()

            # Execute each keyword
            for idx, step in enumerate(keywords, 1):
                keyword = step.get('keyword', '').upper()
                locator_type = step.get('locator_type', '')
                locator_value = step.get('locator_value', '')
                test_data = step.get('test_data', '')
                description = step.get('description', '')

                if not keyword:
                    continue

                self.logger.step(f"Step {idx}: {keyword} - {description}")

                try:
                    self.keyword_engine.execute(
                        keyword,
                        locator_type,
                        locator_value,
                        test_data
                    )
                    result.add_step(idx, keyword, "Passed", description)

                except Exception as step_error:
                    error_msg = str(step_error)
                    result.add_step(idx, keyword, "Failed", error_msg)
                    result.error_message = error_msg
                    result.status = "Failed"

                    # Take screenshot on failure
                    if Config.SCREENSHOT_ON_FAILURE:
                        try:
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            screenshot_name = f"{test_case_id}_step{idx}_{timestamp}"
                            result.screenshot_path = self.keyword_engine.take_screenshot(screenshot_name)
                        except Exception:
                            pass

                    break

            if result.status != "Failed":
                result.status = "Passed"

        except Exception as e:
            result.status = "Error"
            result.error_message = str(e)

        finally:
            result.end_time = datetime.now()
            self._teardown_driver()

        return result

    def _run_test_case(
        self,
        reader: ExcelReader,
        test_case_id: str,
        screen_flow: str,
        description: str
    ) -> TestResult:
        """
        Run test case from Excel data

        Args:
            reader: Excel reader instance
            test_case_id: Test case ID
            screen_flow: Comma-separated screen names
            description: Test description

        Returns:
            Test result
        """
        result = TestResult(test_case_id, description)
        result.start_time = datetime.now()
        result.status = "Running"

        try:
            # Create browser
            self._setup_driver()

            # Parse screen flow
            screens = [s.strip() for s in screen_flow.split(',') if s.strip()]

            # Execute each screen's keywords
            for screen_name in screens:
                self.logger.info(f"Processing screen: {screen_name}")

                try:
                    keywords = reader.read_keywords(screen_name)
                except ValueError:
                    self.logger.warning(f"Screen '{screen_name}' not found, skipping")
                    continue

                for idx, step in enumerate(keywords, 1):
                    keyword = step.get('keyword', '').upper()
                    locator_type = step.get('locator_type', '')
                    locator_value = step.get('locator_value', '')
                    test_data = str(step.get('test_data', '') or '')
                    step_desc = step.get('description', '')

                    if not keyword:
                        continue

                    self.logger.step(f"Step {idx}: {keyword}")

                    try:
                        self.keyword_engine.execute(
                            keyword,
                            locator_type,
                            locator_value,
                            test_data
                        )
                        result.add_step(idx, keyword, "Passed", step_desc)

                    except Exception as step_error:
                        error_msg = str(step_error)
                        result.add_step(idx, keyword, "Failed", error_msg)
                        result.error_message = f"Screen: {screen_name}, Step: {idx} - {error_msg}"
                        result.status = "Failed"

                        # Take screenshot on failure
                        if Config.SCREENSHOT_ON_FAILURE:
                            try:
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                screenshot_name = f"{test_case_id}_{screen_name}_step{idx}_{timestamp}"
                                result.screenshot_path = self.keyword_engine.take_screenshot(screenshot_name)
                            except Exception:
                                pass

                        raise step_error

            if result.status != "Failed":
                result.status = "Passed"

                # Take success screenshot if configured
                if Config.SCREENSHOT_ON_SUCCESS:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    screenshot_name = f"{test_case_id}_success_{timestamp}"
                    result.screenshot_path = self.keyword_engine.take_screenshot(screenshot_name)

        except Exception as e:
            if result.status != "Failed":
                result.status = "Error"
                result.error_message = str(e)

        finally:
            result.end_time = datetime.now()
            self._teardown_driver()

        self.logger.info(f"Test {test_case_id}: {result.status} ({result.duration:.2f}s)")
        return result

    def _setup_driver(self):
        """Setup WebDriver and keyword engine"""
        self.driver = DriverFactory.create_driver(
            browser=self.browser,
            headless=self.headless
        )
        DriverFactory.set_driver(self.driver)
        self.keyword_engine = KeywordEngine(self.driver)

    def _teardown_driver(self):
        """Teardown WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            finally:
                self.driver = None
                self.keyword_engine = None
                DriverFactory.quit_driver()

    def _print_summary(self, duration: float):
        """Print execution summary"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "Passed")
        failed = sum(1 for r in self.results if r.status == "Failed")
        errors = sum(1 for r in self.results if r.status == "Error")
        pass_rate = (passed / total * 100) if total > 0 else 0

        self.logger.info("\n" + "=" * 60)
        self.logger.info("EXECUTION SUMMARY")
        self.logger.info("=" * 60)
        self.logger.info(f"Total Tests: {total}")
        self.logger.info(f"Passed: {passed}")
        self.logger.info(f"Failed: {failed}")
        self.logger.info(f"Errors: {errors}")
        self.logger.info(f"Pass Rate: {pass_rate:.1f}%")
        self.logger.info(f"Duration: {duration:.2f} seconds")
        self.logger.info("=" * 60)

    def generate_report(self, output_path: Path = None) -> str:
        """
        Generate HTML report from results

        Args:
            output_path: Output file path

        Returns:
            Report file path
        """
        from ..utils.report_generator import ReportGenerator
        output_path = output_path or Config.REPORTS_DIR / "keyword_test_report.html"
        report_data = [r.to_dict() for r in self.results]
        return ReportGenerator.generate_html_report(report_data, output_path)
