"""
Main Test Runner Script.
Entry point for executing Selenium test automation framework.
"""

import sys
import argparse
from pathlib import Path

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent))

from framework.core.test_executor import TestExecutor
from framework.utils.logger import Logger


def main():
    """Main function to run tests."""
    parser = argparse.ArgumentParser(
        description='Selenium Python Test Automation Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all test cases marked for execution in Master sheet
  python run_tests.py

  # Run a specific test case by ID
  python run_tests.py --test-case TC001

  # Use a different Excel file
  python run_tests.py --data-file path/to/TestData.xlsx
        """
    )

    parser.add_argument(
        '--test-case',
        type=str,
        help='Run a specific test case by ID (e.g., TC001)'
    )

    parser.add_argument(
        '--data-file',
        type=str,
        help='Path to Excel test data file (overrides config)'
    )

    args = parser.parse_args()

    logger = Logger()

    try:
        # Display framework banner
        print_banner()

        # Create test executor
        executor = TestExecutor()

        # Override Excel path if provided
        if args.data_file:
            from framework.config.config import Config
            Config.TEST_DATA_PATH = Path(args.data_file)
            logger.info(f"Using custom test data file: {args.data_file}")

        # Execute tests
        if args.test_case:
            # Run specific test case
            logger.info(f"Running specific test case: {args.test_case}\n")
            success = executor.execute_single_test(args.test_case)
        else:
            # Run all test cases
            logger.info("Running all test cases from Master sheet\n")
            success = executor.execute_all_tests()

        # Exit with appropriate code
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        logger.warning("\n\nTest execution interrupted by user")
        sys.exit(130)

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def print_banner():
    """Print framework banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              SELENIUM PYTHON TEST AUTOMATION FRAMEWORK                        ║
║              Keyword-Driven Testing with Excel Data Source                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


if __name__ == "__main__":
    main()
