"""
Main execution script for Keyword Driven Test Automation Framework
"""
import sys
import argparse
from pathlib import Path
from framework.core.test_executor import TestExecutor
from framework.utils.logger import logger
from framework.config.config import TEST_DATA_CONFIG

def print_banner():
    """Print framework banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║   Keyword Driven Test Automation Framework                       ║
    ║   Playwright + Python                                             ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Main execution function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Keyword Driven Test Automation Framework')
    parser.add_argument(
        '--testdata',
        type=str,
        default=None,
        help='Path to test data Excel file (default: test_data/TestData.xlsx)'
    )
    parser.add_argument(
        '--browser',
        type=str,
        choices=['chromium', 'firefox', 'webkit'],
        default=None,
        help='Browser to use for testing'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )

    args = parser.parse_args()

    # Update browser config if provided
    if args.browser:
        from framework.config import config
        config.BROWSER_CONFIG['browser'] = args.browser

    if args.headless:
        from framework.config import config
        config.BROWSER_CONFIG['headless'] = True

    # Print banner
    print_banner()

    # Get test data file path
    test_data_file = args.testdata

    if test_data_file and not Path(test_data_file).exists():
        logger.error(f"Test data file not found: {test_data_file}")
        sys.exit(1)

    # Check if default test data file exists
    if not test_data_file:
        default_file = Path(TEST_DATA_CONFIG["test_data_file"])
        if not default_file.exists():
            logger.error(f"Default test data file not found: {default_file}")
            logger.info("Please create test data file using: python create_sample_testdata.py")
            sys.exit(1)

    try:
        # Create test executor
        executor = TestExecutor(test_data_file)

        # Execute all tests
        success = executor.execute_all_tests()

        # Cleanup
        executor.cleanup()

        # Exit with appropriate code
        if success:
            logger.info("\n✓ Test execution completed successfully!")
            sys.exit(0)
        else:
            logger.error("\n✗ Test execution completed with errors!")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.warning("\nTest execution interrupted by user")
        if 'executor' in locals():
            executor.cleanup()
        sys.exit(1)

    except Exception as e:
        logger.error(f"\nUnexpected error: {str(e)}")
        if 'executor' in locals():
            executor.cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()
