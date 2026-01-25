#!/usr/bin/env python3
"""
Main entry point for running Selenium Behave tests
Supports both BDD (Behave) and Keyword-driven execution
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_behave_tests(tags=None, features=None, dry_run=False, verbose=False):
    """
    Run Behave BDD tests

    Args:
        tags: Test tags to run (e.g., '@smoke', '@login')
        features: Specific feature files or directories
        dry_run: Parse features without executing
        verbose: Enable verbose output
    """
    cmd = ["behave"]

    # Add configuration file
    config_file = Path(__file__).parent / "behave.ini"
    if config_file.exists():
        cmd.extend(["-c", str(config_file)])

    # Add tags
    if tags:
        for tag in tags:
            cmd.extend(["--tags", tag])

    # Add features
    if features:
        cmd.extend(features)
    else:
        cmd.append("selenium_behave_framework/features")

    # Add options
    if dry_run:
        cmd.append("--dry-run")

    if verbose:
        cmd.append("-v")

    # Add output format for reports
    cmd.extend(["--format", "pretty"])
    cmd.extend(["--format", "json", "-o", "reports/behave_report.json"])

    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=Path(__file__).parent.parent)


def run_keyword_tests(test_data=None, browser=None, headless=False):
    """
    Run keyword-driven tests

    Args:
        test_data: Path to test data Excel file
        browser: Browser to use
        headless: Run in headless mode
    """
    # Import here to avoid circular imports
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from selenium_behave_framework.keywords.keyword_executor import KeywordExecutor
    from selenium_behave_framework.config.config import Config

    test_data_path = Path(test_data) if test_data else Config.get_test_data_path()

    if not test_data_path.exists():
        print(f"Test data file not found: {test_data_path}")
        print("Creating sample test data...")
        from create_sample_testdata import create_sample_test_data
        create_sample_test_data()

    executor = KeywordExecutor(
        test_data_path=test_data_path,
        browser=browser or Config.BROWSER,
        headless=headless
    )

    results = executor.run_all_tests()
    report_path = executor.generate_report()

    print(f"\nReport generated: {report_path}")
    return results


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Selenium Behave POM Framework - Test Runner"
    )

    parser.add_argument(
        "--mode",
        choices=["behave", "keyword", "both"],
        default="behave",
        help="Test execution mode (default: behave)"
    )

    parser.add_argument(
        "--tags",
        nargs="+",
        help="Behave tags to run (e.g., @smoke @login)"
    )

    parser.add_argument(
        "--features",
        nargs="+",
        help="Feature files or directories to run"
    )

    parser.add_argument(
        "--testdata",
        help="Path to keyword test data Excel file"
    )

    parser.add_argument(
        "--browser",
        choices=["chrome", "firefox", "edge"],
        default="chrome",
        help="Browser to use (default: chrome)"
    )

    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse features without executing (Behave only)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--create-testdata",
        action="store_true",
        help="Create sample test data file and exit"
    )

    args = parser.parse_args()

    # Create sample test data if requested
    if args.create_testdata:
        from create_sample_testdata import create_sample_test_data
        create_sample_test_data()
        return

    # Run tests based on mode
    if args.mode == "behave":
        result = run_behave_tests(
            tags=args.tags,
            features=args.features,
            dry_run=args.dry_run,
            verbose=args.verbose
        )
        sys.exit(result.returncode)

    elif args.mode == "keyword":
        results = run_keyword_tests(
            test_data=args.testdata,
            browser=args.browser,
            headless=args.headless
        )
        # Exit with error if any tests failed
        failed = any(r.status != "Passed" for r in results)
        sys.exit(1 if failed else 0)

    elif args.mode == "both":
        print("=" * 60)
        print("Running Behave BDD Tests")
        print("=" * 60)
        behave_result = run_behave_tests(
            tags=args.tags,
            features=args.features,
            dry_run=args.dry_run,
            verbose=args.verbose
        )

        print("\n" + "=" * 60)
        print("Running Keyword-Driven Tests")
        print("=" * 60)
        keyword_results = run_keyword_tests(
            test_data=args.testdata,
            browser=args.browser,
            headless=args.headless
        )

        # Exit with error if any tests failed
        keyword_failed = any(r.status != "Passed" for r in keyword_results)
        sys.exit(1 if behave_result.returncode != 0 or keyword_failed else 0)


if __name__ == "__main__":
    main()
