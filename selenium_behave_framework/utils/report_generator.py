"""
Report Generator for creating HTML test reports
"""

from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

from ..config.config import Config


class ReportGenerator:
    """Generates HTML test reports"""

    @staticmethod
    def generate_html_report(
        results: List[Dict[str, Any]],
        output_path: Path = None
    ) -> str:
        """
        Generate HTML report from test results

        Args:
            results: List of test result dictionaries
            output_path: Output file path

        Returns:
            Path to generated report
        """
        output_path = output_path or Config.REPORTS_DIR / "test_report.html"

        # Calculate summary
        total = len(results)
        passed = sum(1 for r in results if r.get('status') == 'Passed')
        failed = sum(1 for r in results if r.get('status') == 'Failed')
        errors = sum(1 for r in results if r.get('status') == 'Error')
        pass_rate = (passed / total * 100) if total > 0 else 0
        total_duration = sum(r.get('duration', 0) for r in results)

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Selenium Behave Test Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .header h1 {{
            font-size: 2rem;
            margin-bottom: 10px;
        }}
        .header p {{
            opacity: 0.9;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .summary-card h3 {{
            font-size: 2rem;
            margin-bottom: 5px;
        }}
        .summary-card.passed h3 {{ color: #28a745; }}
        .summary-card.failed h3 {{ color: #dc3545; }}
        .summary-card.total h3 {{ color: #667eea; }}
        .summary-card.rate h3 {{ color: #17a2b8; }}
        .results-table {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #555;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .status {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        .status.passed {{
            background: #d4edda;
            color: #155724;
        }}
        .status.failed {{
            background: #f8d7da;
            color: #721c24;
        }}
        .status.error {{
            background: #fff3cd;
            color: #856404;
        }}
        .expandable {{
            cursor: pointer;
        }}
        .expandable:hover {{
            background: #e9ecef;
        }}
        .steps {{
            display: none;
            padding: 15px;
            background: #f8f9fa;
        }}
        .steps.show {{
            display: block;
        }}
        .step-item {{
            padding: 10px;
            margin: 5px 0;
            background: white;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }}
        .step-item.passed {{ border-left-color: #28a745; }}
        .step-item.failed {{ border-left-color: #dc3545; }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9rem;
        }}
        .error-message {{
            color: #dc3545;
            font-size: 0.85rem;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Selenium Behave Test Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Duration: {total_duration:.2f} seconds</p>
        </div>

        <div class="summary">
            <div class="summary-card total">
                <h3>{total}</h3>
                <p>Total Tests</p>
            </div>
            <div class="summary-card passed">
                <h3>{passed}</h3>
                <p>Passed</p>
            </div>
            <div class="summary-card failed">
                <h3>{failed}</h3>
                <p>Failed</p>
            </div>
            <div class="summary-card rate">
                <h3>{pass_rate:.1f}%</h3>
                <p>Pass Rate</p>
            </div>
        </div>

        <div class="results-table">
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Test Case</th>
                        <th>Description</th>
                        <th>Duration</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
"""

        for idx, result in enumerate(results, 1):
            status = result.get('status', 'Unknown')
            status_class = status.lower()
            test_id = result.get('test_case_id', f'Test_{idx}')
            description = result.get('description', '')
            duration = result.get('duration', 0)
            error_msg = result.get('error_message', '')
            steps = result.get('steps', [])

            html_content += f"""
                    <tr class="expandable" onclick="toggleSteps('steps-{idx}')">
                        <td>{idx}</td>
                        <td>{test_id}</td>
                        <td>{description}</td>
                        <td>{duration:.2f}s</td>
                        <td><span class="status {status_class}">{status}</span></td>
                    </tr>
                    <tr>
                        <td colspan="5" class="steps" id="steps-{idx}">
"""
            if error_msg:
                html_content += f'<div class="error-message"><strong>Error:</strong> {error_msg}</div>'

            for step in steps:
                step_status = step.get('status', '').lower()
                step_keyword = step.get('keyword', '')
                step_msg = step.get('message', '')
                html_content += f"""
                            <div class="step-item {step_status}">
                                <strong>Step {step.get('step_no', '')}:</strong> {step_keyword}
                                <span class="status {step_status}">{step.get('status', '')}</span>
                                {f'<br><small>{step_msg}</small>' if step_msg else ''}
                            </div>
"""

            html_content += """
                        </td>
                    </tr>
"""

        html_content += """
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>Selenium Behave POM Framework - Test Automation Report</p>
        </div>
    </div>

    <script>
        function toggleSteps(id) {
            const element = document.getElementById(id);
            element.classList.toggle('show');
        }
    </script>
</body>
</html>
"""

        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(output_path)
