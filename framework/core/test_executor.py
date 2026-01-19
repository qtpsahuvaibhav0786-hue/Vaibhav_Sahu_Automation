"""
Test Executor module - Orchestrates test execution
"""
from framework.core.excel_reader import ExcelReader
from framework.core.browser_manager import BrowserManager
from framework.keywords.keyword_engine import KeywordEngine
from framework.utils.logger import logger
from framework.utils.report_generator import ReportGenerator
from framework.config.config import EXECUTION_CONFIG

class TestExecutor:
    """
    Main test executor that:
    1. Reads test cases from Master Sheet
    2. Loads screen data for each test case
    3. Executes keywords for each screen in the flow
    4. Generates test reports
    """

    def __init__(self, test_data_file=None):
        self.excel_reader = ExcelReader(test_data_file)
        self.browser_manager = BrowserManager()
        self.keyword_engine = None
        self.report_generator = ReportGenerator()
        self.test_results = []

    def initialize(self):
        """Initialize test execution environment"""
        try:
            logger.info("="*80)
            logger.info("Initializing Test Execution Environment")
            logger.info("="*80)

            # Load workbook
            if not self.excel_reader.load_workbook():
                logger.error("Failed to load test data workbook")
                return False

            # Read master sheet
            test_cases = self.excel_reader.read_master_sheet()
            if not test_cases:
                logger.error("No test cases selected for execution")
                return False

            logger.info(f"Total test cases to execute: {len(test_cases)}")
            return True

        except Exception as e:
            logger.error(f"Error during initialization: {str(e)}")
            return False

    def execute_test_case(self, test_case_data):
        """
        Execute a single test case
        test_case_data: Dictionary from master sheet row
        """
        try:
            test_case_id = test_case_data.get('TestCaseID', 'Unknown')
            screen_flow = test_case_data.get('ScreenFlow', '')
            description = test_case_data.get('Description', '')

            logger.test_start(f"{test_case_id} - {description}")

            # Start browser for this test case
            if not self.browser_manager.start_browser():
                logger.error("Failed to start browser")
                return False, "Browser start failed"

            # Initialize keyword engine
            self.keyword_engine = KeywordEngine(self.browser_manager)

            # Get test data for the screen flow
            flow_data = self.excel_reader.get_test_data_for_flow(screen_flow)

            if not flow_data:
                logger.error(f"No test data found for screen flow: {screen_flow}")
                self.browser_manager.close_browser()
                return False, f"No data for screen flow: {screen_flow}"

            # Execute each screen in the flow
            overall_status = "PASS"
            error_message = ""

            for screen_data in flow_data:
                screen_name = screen_data['screen_name']
                logger.info(f"\n--- Executing Screen: {screen_name} ---")

                # Get the first test case from screen (or you can modify to use specific test case)
                if screen_data['test_cases']:
                    test_case = screen_data['test_cases'][0]  # Using first test case

                    # Execute each step in the test case
                    for step in test_case['steps']:
                        field = step['field']
                        locator = step['locator']
                        keyword = step['keyword']
                        value = step['value']

                        # Execute keyword
                        success, message = self.keyword_engine.execute_keyword(keyword, locator, value)

                        if success:
                            logger.step_result("PASS", message)
                        else:
                            logger.step_result("FAIL", message)
                            overall_status = "FAIL"
                            error_message = message

                            # Take screenshot on failure
                            if EXECUTION_CONFIG["screenshot_on_failure"]:
                                screenshot_path = self.browser_manager.take_screenshot(
                                    f"{test_case_id}_{screen_name}_FAILED"
                                )

                            # Stop execution on first failure (optional)
                            break

                    if overall_status == "FAIL":
                        break  # Stop flow if any screen fails

            # Take screenshot on success if configured
            screenshot_path = ""
            if overall_status == "PASS" and EXECUTION_CONFIG["screenshot_on_success"]:
                screenshot_path = self.browser_manager.take_screenshot(f"{test_case_id}_PASSED")
            elif overall_status == "FAIL" and EXECUTION_CONFIG["screenshot_on_failure"]:
                screenshot_path = self.browser_manager.take_screenshot(f"{test_case_id}_FAILED")

            # Close browser after test case
            self.browser_manager.close_browser()

            # Add to report
            self.report_generator.add_test_result(
                test_case=test_case_id,
                screen_flow=screen_flow,
                status=overall_status,
                error_message=error_message,
                screenshot_path=screenshot_path
            )

            logger.test_end(test_case_id, overall_status)

            return overall_status == "PASS", error_message

        except Exception as e:
            error_msg = f"Error executing test case: {str(e)}"
            logger.error(error_msg)

            # Close browser on exception
            if self.browser_manager:
                self.browser_manager.close_browser()

            return False, error_msg

    def execute_all_tests(self):
        """Execute all selected test cases"""
        try:
            # Initialize
            if not self.initialize():
                logger.error("Initialization failed. Aborting test execution.")
                return False

            # Get all test cases
            test_cases = self.excel_reader.get_all_test_cases()

            # Start execution timer
            self.report_generator.start_execution()

            logger.info("\n" + "="*80)
            logger.info("Starting Test Execution")
            logger.info("="*80 + "\n")

            # Execute each test case
            for test_case in test_cases:
                self.execute_test_case(test_case)

            # End execution timer
            self.report_generator.end_execution()

            # Generate report
            report_path = self.report_generator.generate_report()
            logger.info(f"\n{'='*80}")
            logger.info(f"Test execution completed!")
            logger.info(f"Report generated: {report_path}")
            logger.info(f"{'='*80}")

            # Close workbook
            self.excel_reader.close_workbook()

            return True

        except Exception as e:
            logger.error(f"Error during test execution: {str(e)}")
            return False

    def cleanup(self):
        """Cleanup resources"""
        try:
            if self.browser_manager:
                self.browser_manager.close_browser()
            if self.excel_reader:
                self.excel_reader.close_workbook()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
