"""
Test Executor Module.
Orchestrates the entire test execution workflow.
"""

import datetime
from pathlib import Path

from framework.config.config import Config
from framework.core.selenium_driver import SeleniumDriver
from framework.core.excel_reader import ExcelReader
from framework.keywords.keyword_engine import KeywordEngine
from framework.utils.logger import Logger
from framework.utils.report_generator import ReportGenerator


class TestExecutor:
    """Manages test execution workflow."""

    def __init__(self):
        """Initialize Test Executor."""
        self.logger = Logger()
        self.excel_reader = None
        self.test_cases = []
        self.report_generator = ReportGenerator()
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

    def initialize(self):
        """
        Initialize test executor by loading test data.

        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            self.logger.info("=" * 80)
            self.logger.info("SELENIUM TEST AUTOMATION FRAMEWORK - INITIALIZATION")
            self.logger.info("=" * 80)

            # Ensure required directories exist
            Config.ensure_directories()
            self.logger.success("Required directories verified")

            # Display configuration
            self.logger.info("\nConfiguration Summary:")
            config_summary = Config.get_config_summary()
            for key, value in config_summary.items():
                self.logger.info(f"  {key}: {value}")

            # Load Excel file
            self.logger.info("\nLoading test data...")
            self.excel_reader = ExcelReader()

            if not self.excel_reader.load_workbook():
                self.logger.error("Failed to load Excel workbook")
                return False

            # Validate Excel structure
            is_valid, errors = self.excel_reader.validate_excel_structure()
            if not is_valid:
                self.logger.error("Excel validation failed:")
                for error in errors:
                    self.logger.error(f"  - {error}")
                return False

            self.logger.success("Excel structure validated")

            # Read Master sheet
            self.test_cases = self.excel_reader.read_master_sheet()

            if not self.test_cases:
                self.logger.warning("No test cases found to execute")
                return False

            self.total_tests = len(self.test_cases)
            self.logger.success(f"Found {self.total_tests} test case(s) to execute\n")

            # Display test cases
            self.logger.info("Test Cases to Execute:")
            for idx, test_case in enumerate(self.test_cases, 1):
                tc_id = test_case.get("TestCaseID", "N/A")
                description = test_case.get("Description", "N/A")
                screen_flow = test_case.get("ScreenFlow", "N/A")
                self.logger.info(f"  {idx}. {tc_id} - {description} [{screen_flow}]")

            self.logger.info("\nInitialization completed successfully")
            self.logger.info("=" * 80 + "\n")

            return True

        except Exception as e:
            self.logger.error(f"Initialization failed: {str(e)}")
            return False

    def execute_test_case(self, test_case_data):
        """
        Execute a single test case.

        Args:
            test_case_data (dict): Test case information from Master sheet

        Returns:
            bool: True if test case passed, False otherwise
        """
        tc_id = test_case_data.get("TestCaseID", "Unknown")
        description = test_case_data.get("Description", "No description")
        screen_flow = test_case_data.get("ScreenFlow", "")

        self.logger.test_start(tc_id, description)

        driver_manager = None
        test_passed = True
        failure_reason = ""
        screenshot_path = None

        try:
            # Initialize browser
            driver_manager = SeleniumDriver()
            if not driver_manager.start_browser():
                raise Exception("Failed to start browser")

            # Initialize keyword engine
            keyword_engine = KeywordEngine(driver_manager)

            # Get test data for screen flow
            flow_data = self.excel_reader.get_test_data_for_flow(screen_flow)

            if not flow_data:
                raise Exception(f"No test data found for screen flow: {screen_flow}")

            # Execute each screen in the flow
            for screen_data in flow_data:
                screen_name = screen_data.get("screen_name", "Unknown")
                self.logger.info(f"\n  Executing Screen: {screen_name}")
                self.logger.info("  " + "-" * 70)

                # Parse test steps from screen data
                test_steps = self.excel_reader.parse_test_steps(screen_data)

                if not test_steps:
                    self.logger.warning(f"  No test steps found for screen: {screen_name}")
                    continue

                # Execute each test step
                for step_idx, step in enumerate(test_steps, 1):
                    keyword = step.get("keyword", "")
                    locator = step.get("locator", "")
                    value = step.get("value", "")
                    field_name = step.get("field_name", "")

                    # Log keyword execution
                    self.logger.keyword_execution(step_idx, keyword, field_name, locator, value)

                    # Execute keyword
                    success, message = keyword_engine.execute_keyword(keyword, locator, value)

                    # Log result
                    self.logger.step_result(success, message)

                    if not success:
                        test_passed = False
                        failure_reason = f"Step {step_idx} failed: {message}"
                        self.logger.error(f"  Test case failed at step {step_idx}")
                        break

                # Break if test failed
                if not test_passed:
                    break

            # Take screenshot
            screenshot_name = f"{tc_id}_{'PASS' if test_passed else 'FAIL'}"
            if (test_passed and Config.SCREENSHOT_ON_SUCCESS) or \
               (not test_passed and Config.SCREENSHOT_ON_FAILURE):
                screenshot_path = driver_manager.take_screenshot(screenshot_name)

        except Exception as e:
            test_passed = False
            failure_reason = str(e)
            self.logger.error(f"  Test execution error: {str(e)}")

            # Take screenshot on exception
            if driver_manager and Config.SCREENSHOT_ON_FAILURE:
                try:
                    screenshot_path = driver_manager.take_screenshot(f"{tc_id}_ERROR")
                except:
                    pass

        finally:
            # Close browser
            if driver_manager:
                driver_manager.close_browser()

        # Update counters
        if test_passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1

        # Log test result
        self.logger.test_end(test_passed)

        # Add to report
        self.report_generator.add_test_result(
            test_case_id=tc_id,
            description=description,
            status="PASS" if test_passed else "FAIL",
            duration=0,  # Duration tracking can be added
            screenshot=screenshot_path,
            error_message=failure_reason if not test_passed else ""
        )

        return test_passed

    def execute_all_tests(self):
        """
        Execute all test cases from the Master sheet.

        Returns:
            bool: True if all tests passed, False otherwise
        """
        try:
            if not self.initialize():
                self.logger.error("Test execution aborted due to initialization failure")
                return False

            # Start execution timer
            start_time = datetime.datetime.now()
            self.report_generator.start_execution()

            self.logger.info("=" * 80)
            self.logger.info("STARTING TEST EXECUTION")
            self.logger.info("=" * 80 + "\n")

            # Execute each test case
            for idx, test_case in enumerate(self.test_cases, 1):
                self.logger.info(f"\n{'=' * 80}")
                self.logger.info(f"Executing Test Case {idx} of {self.total_tests}")
                self.logger.info(f"{'=' * 80}\n")

                self.execute_test_case(test_case)

            # End execution timer
            end_time = datetime.datetime.now()
            duration = (end_time - start_time).total_seconds()
            self.report_generator.end_execution()

            # Display summary
            self.logger.info("\n" + "=" * 80)
            self.logger.info("TEST EXECUTION SUMMARY")
            self.logger.info("=" * 80)
            self.logger.info(f"Total Test Cases: {self.total_tests}")
            self.logger.info(f"Passed: {self.passed_tests}")
            self.logger.info(f"Failed: {self.failed_tests}")
            self.logger.info(f"Pass Rate: {(self.passed_tests/self.total_tests*100):.2f}%")
            self.logger.info(f"Execution Time: {duration:.2f} seconds")
            self.logger.info("=" * 80 + "\n")

            # Generate HTML report
            self.logger.info("Generating HTML report...")
            report_path = self.report_generator.generate_report()

            if report_path:
                self.logger.success(f"HTML report generated: {report_path}")
            else:
                self.logger.warning("Failed to generate HTML report")

            # Return overall result
            all_passed = self.failed_tests == 0

            if all_passed:
                self.logger.success("\n✓ ALL TESTS PASSED!")
            else:
                self.logger.error(f"\n✗ {self.failed_tests} TEST(S) FAILED!")

            return all_passed

        except Exception as e:
            self.logger.error(f"Test execution failed: {str(e)}")
            return False

        finally:
            self.cleanup()

    def cleanup(self):
        """Release resources and perform cleanup."""
        try:
            if self.excel_reader:
                self.excel_reader.close_workbook()
            self.logger.info("\nCleanup completed")
        except Exception as e:
            self.logger.warning(f"Cleanup error: {str(e)}")

    def execute_single_test(self, test_case_id):
        """
        Execute a specific test case by ID.

        Args:
            test_case_id (str): Test case ID to execute

        Returns:
            bool: True if test passed, False otherwise
        """
        try:
            if not self.initialize():
                return False

            # Find test case by ID
            test_case = None
            for tc in self.test_cases:
                if tc.get("TestCaseID") == test_case_id:
                    test_case = tc
                    break

            if not test_case:
                self.logger.error(f"Test case '{test_case_id}' not found or not marked for execution")
                return False

            self.logger.info(f"\nExecuting single test case: {test_case_id}")
            self.report_generator.start_execution()

            result = self.execute_test_case(test_case)

            self.report_generator.end_execution()
            self.report_generator.generate_report()

            return result

        except Exception as e:
            self.logger.error(f"Failed to execute test case: {str(e)}")
            return False

        finally:
            self.cleanup()
