"""
Report generator module for creating HTML test reports
"""
from datetime import datetime
from pathlib import Path
from framework.config.config import REPORT_CONFIG

class ReportGenerator:
    """Generate HTML report for test execution"""

    def __init__(self):
        self.test_results = []
        self.start_time = None
        self.end_time = None

    def start_execution(self):
        """Mark execution start time"""
        self.start_time = datetime.now()

    def end_execution(self):
        """Mark execution end time"""
        self.end_time = datetime.now()

    def add_test_result(self, test_case, screen_flow, status, error_message="", screenshot_path=""):
        """Add test result to the report"""
        result = {
            "test_case": test_case,
            "screen_flow": screen_flow,
            "status": status,
            "error_message": error_message,
            "screenshot_path": screenshot_path,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)

    def generate_report(self):
        """Generate HTML report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed_tests = sum(1 for r in self.test_results if r["status"] == "FAIL")
        pass_percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        duration = (self.end_time - self.start_time).total_seconds() if self.end_time and self.start_time else 0

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{REPORT_CONFIG["report_title"]}</title>
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
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
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
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .summary-card h3 {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}
        .summary-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }}
        .summary-card.total {{ border-left: 4px solid #3498db; }}
        .summary-card.passed {{ border-left: 4px solid #2ecc71; }}
        .summary-card.failed {{ border-left: 4px solid #e74c3c; }}
        .summary-card.percentage {{ border-left: 4px solid #f39c12; }}
        .summary-card.duration {{ border-left: 4px solid #9b59b6; }}
        .results {{
            padding: 30px;
        }}
        .results h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .status {{
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.85em;
            display: inline-block;
        }}
        .status.pass {{
            background: #d4edda;
            color: #155724;
        }}
        .status.fail {{
            background: #f8d7da;
            color: #721c24;
        }}
        .error-message {{
            color: #e74c3c;
            font-size: 0.9em;
            font-style: italic;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        .screenshot-link {{
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
        }}
        .screenshot-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{REPORT_CONFIG["report_title"]}</h1>
            <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
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
            <div class="summary-card percentage">
                <h3>Pass Rate</h3>
                <div class="value">{pass_percentage:.1f}%</div>
            </div>
            <div class="summary-card duration">
                <h3>Duration</h3>
                <div class="value">{duration:.1f}s</div>
            </div>
        </div>

        <div class="results">
            <h2>Test Results Details</h2>
            <table>
                <thead>
                    <tr>
                        <th>Test Case</th>
                        <th>Screen Flow</th>
                        <th>Status</th>
                        <th>Timestamp</th>
                        <th>Error Message</th>
                        <th>Screenshot</th>
                    </tr>
                </thead>
                <tbody>
"""

        for result in self.test_results:
            status_class = "pass" if result["status"] == "PASS" else "fail"
            screenshot_html = ""
            if result["screenshot_path"]:
                screenshot_html = f'<a href="{result["screenshot_path"]}" class="screenshot-link" target="_blank">View</a>'

            html_content += f"""
                    <tr>
                        <td>{result["test_case"]}</td>
                        <td>{result["screen_flow"]}</td>
                        <td><span class="status {status_class}">{result["status"]}</span></td>
                        <td>{result["timestamp"]}</td>
                        <td class="error-message">{result["error_message"]}</td>
                        <td>{screenshot_html}</td>
                    </tr>
"""

        html_content += """
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>Keyword Driven Test Automation Framework | Playwright + Python</p>
        </div>
    </div>
</body>
</html>
"""

        # Save report
        report_path = Path(REPORT_CONFIG["report_path"]) / REPORT_CONFIG["report_name"]
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(report_path)
