"""
Report Generator Module.
Generates beautiful HTML reports for test execution results.
"""

import datetime
from pathlib import Path
from framework.config.config import Config
from framework.utils.logger import Logger


class ReportGenerator:
    """Generates HTML test execution reports."""

    def __init__(self):
        """Initialize Report Generator."""
        self.test_results = []
        self.start_time = None
        self.end_time = None
        self.logger = Logger()

    def start_execution(self):
        """Mark the start of test execution."""
        self.start_time = datetime.datetime.now()

    def end_execution(self):
        """Mark the end of test execution."""
        self.end_time = datetime.datetime.now()

    def add_test_result(self, test_case_id, description, status, duration, screenshot=None, error_message=""):
        """
        Add a test result to the report.

        Args:
            test_case_id (str): Test case ID
            description (str): Test case description
            status (str): Test status (PASS/FAIL)
            duration (float): Test execution duration in seconds
            screenshot (str): Path to screenshot file
            error_message (str): Error message if test failed
        """
        result = {
            "test_case_id": test_case_id,
            "description": description,
            "status": status,
            "duration": duration,
            "screenshot": screenshot,
            "error_message": error_message,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)

    def generate_report(self):
        """
        Generate HTML report.

        Returns:
            str: Path to generated report file
        """
        try:
            # Calculate statistics
            total_tests = len(self.test_results)
            passed_tests = sum(1 for r in self.test_results if r["status"] == "PASS")
            failed_tests = total_tests - passed_tests
            pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

            # Calculate duration
            if self.start_time and self.end_time:
                duration = (self.end_time - self.start_time).total_seconds()
                duration_str = f"{duration:.2f} seconds"
            else:
                duration_str = "N/A"

            # Generate HTML content
            html_content = self._generate_html(
                total_tests=total_tests,
                passed_tests=passed_tests,
                failed_tests=failed_tests,
                pass_rate=pass_rate,
                duration=duration_str,
                start_time=self.start_time.strftime("%Y-%m-%d %H:%M:%S") if self.start_time else "N/A",
                end_time=self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else "N/A"
            )

            # Write to file
            Config.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
            report_path = Config.REPORT_FILE

            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            return str(report_path)

        except Exception as e:
            self.logger.error(f"Failed to generate report: {str(e)}")
            return None

    def _generate_html(self, total_tests, passed_tests, failed_tests, pass_rate, duration, start_time, end_time):
        """
        Generate HTML report content.

        Args:
            total_tests (int): Total number of tests
            passed_tests (int): Number of passed tests
            failed_tests (int): Number of failed tests
            pass_rate (float): Pass rate percentage
            duration (str): Execution duration
            start_time (str): Execution start time
            end_time (str): Execution end time

        Returns:
            str: HTML content
        """
        # Generate test result rows
        result_rows = ""
        for idx, result in enumerate(self.test_results, 1):
            status_class = "pass" if result["status"] == "PASS" else "fail"
            status_icon = "✓" if result["status"] == "PASS" else "✗"

            # Screenshot column
            screenshot_cell = ""
            if result["screenshot"]:
                screenshot_path = Path(result["screenshot"])
                if screenshot_path.exists():
                    # Use relative path from reports directory
                    rel_path = Path("..") / "screenshots" / screenshot_path.name
                    screenshot_cell = f'<a href="{rel_path}" target="_blank" class="screenshot-link">View Screenshot</a>'
                else:
                    screenshot_cell = "N/A"
            else:
                screenshot_cell = "N/A"

            # Error message
            error_cell = result["error_message"] if result["error_message"] else "-"

            result_rows += f"""
            <tr class="{status_class}">
                <td>{idx}</td>
                <td>{result["test_case_id"]}</td>
                <td>{result["description"]}</td>
                <td><span class="status-badge {status_class}">{status_icon} {result["status"]}</span></td>
                <td>{result["timestamp"]}</td>
                <td>{screenshot_cell}</td>
                <td class="error-message">{error_cell}</td>
            </tr>
            """

        # Generate full HTML
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{Config.REPORT_TITLE}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}

        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}

        .summary-card h3 {{
            color: #6c757d;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}

        .summary-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }}

        .summary-card.total .value {{ color: #667eea; }}
        .summary-card.passed .value {{ color: #28a745; }}
        .summary-card.failed .value {{ color: #dc3545; }}
        .summary-card.pass-rate .value {{ color: #17a2b8; }}

        .execution-info {{
            padding: 20px 30px;
            background: #fff;
            border-bottom: 1px solid #e9ecef;
        }}

        .execution-info h2 {{
            color: #333;
            margin-bottom: 15px;
            font-size: 1.5em;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }}

        .info-item {{
            display: flex;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
        }}

        .info-item strong {{
            color: #667eea;
            margin-right: 10px;
            min-width: 120px;
        }}

        .results-section {{
            padding: 30px;
        }}

        .results-section h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            overflow: hidden;
        }}

        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        thead th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
        }}

        tbody td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e9ecef;
        }}

        tbody tr:hover {{
            background: #f8f9fa;
        }}

        tbody tr.pass {{
            border-left: 4px solid #28a745;
        }}

        tbody tr.fail {{
            border-left: 4px solid #dc3545;
        }}

        .status-badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.85em;
        }}

        .status-badge.pass {{
            background: #d4edda;
            color: #155724;
        }}

        .status-badge.fail {{
            background: #f8d7da;
            color: #721c24;
        }}

        .screenshot-link {{
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }}

        .screenshot-link:hover {{
            text-decoration: underline;
        }}

        .error-message {{
            color: #dc3545;
            font-size: 0.9em;
            max-width: 300px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            .summary {{
                grid-template-columns: 1fr;
            }}

            table {{
                font-size: 0.85em;
            }}

            thead th, tbody td {{
                padding: 8px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{Config.REPORT_TITLE}</h1>
            <p>Selenium Python Test Automation Framework</p>
        </div>

        <div class="summary">
            <div class="summary-card total">
                <h3>Total Tests</h3>
                <div class="value">{total_tests}</div>
            </div>
            <div class="summary-card passed">
                <h3>Passed</h3>
                <div class="value">{passed_tests}</div>
            </div>
            <div class="summary-card failed">
                <h3>Failed</h3>
                <div class="value">{failed_tests}</div>
            </div>
            <div class="summary-card pass-rate">
                <h3>Pass Rate</h3>
                <div class="value">{pass_rate:.1f}%</div>
            </div>
        </div>

        <div class="execution-info">
            <h2>Execution Information</h2>
            <div class="info-grid">
                <div class="info-item">
                    <strong>Start Time:</strong>
                    <span>{start_time}</span>
                </div>
                <div class="info-item">
                    <strong>End Time:</strong>
                    <span>{end_time}</span>
                </div>
                <div class="info-item">
                    <strong>Duration:</strong>
                    <span>{duration}</span>
                </div>
                <div class="info-item">
                    <strong>Browser:</strong>
                    <span>{Config.BROWSER.upper()}</span>
                </div>
                <div class="info-item">
                    <strong>Headless Mode:</strong>
                    <span>{Config.HEADLESS}</span>
                </div>
                <div class="info-item">
                    <strong>Test Data:</strong>
                    <span>{Config.TEST_DATA_FILE}</span>
                </div>
            </div>
        </div>

        <div class="results-section">
            <h2>Test Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Test Case ID</th>
                        <th>Description</th>
                        <th>Status</th>
                        <th>Timestamp</th>
                        <th>Screenshot</th>
                        <th>Error Message</th>
                    </tr>
                </thead>
                <tbody>
                    {result_rows}
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>Generated by Selenium Python Test Automation Framework</p>
            <p>© {datetime.datetime.now().year} - All Rights Reserved</p>
        </div>
    </div>
</body>
</html>
        """

        return html
