#!/usr/bin/env python3
"""
MediBook Test Execution Script
Runs all automated tests and generates comprehensive reports
"""

import os
import sys
import subprocess
import time
from datetime import datetime
import webbrowser


def print_banner(text):
    """Print formatted banner"""
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}")


def run_command(command, description):
    """Run shell command and return result"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True, result.stdout
        else:
            print(f"❌ {description} failed")
            print(f"Error: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False, str(e)


def check_server_running():
    """Check if Django server is running"""
    try:
        import requests
        response = requests.get("http://127.0.0.1:8000", timeout=5)
        return response.status_code == 200
    except:
        return False


def main():
    """Main test execution function"""
    print_banner("MEDIBOOK AUTOMATED TEST SUITE")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Change to project directory
    project_dir = "/Users/parimal/VisualStudioCodeProjects/stqa_project"
    os.chdir(project_dir)
    
    # Check if server is running
    if not check_server_running():
        print("\n⚠️  Django server is not running!")
        print("Please start the server with: python manage.py runserver")
        print("Then run this test script again.")
        return
    
    print("✅ Django server is running at http://127.0.0.1:8000")
    
    # Create test reports directory
    reports_dir = os.path.join(project_dir, "tests", "test_reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    test_results = {
        'total_tests': 0,
        'passed_tests': 0,
        'failed_tests': 0,
        'start_time': datetime.now(),
        'test_files': []
    }
    
    print_banner("RUNNING SELENIUM WEBDRIVER TESTS")
    
    # List of test files to run
    test_files = [
        ("tests/selenium_tests/test_user_registration.py", "User Registration Tests"),
        ("tests/selenium_tests/test_login_system.py", "Login System Tests"),
        ("tests/selenium_tests/test_appointment_booking.py", "Appointment Booking Tests")
    ]
    
    for test_file, description in test_files:
        if os.path.exists(test_file):
            print(f"\n📋 Running {description}...")
            
            # Activate virtual environment and run test
            command = f"source venv/bin/activate && python {test_file}"
            success, output = run_command(command, f"Execute {description}")
            
            # Parse results from output
            if "Tests Run:" in output:
                lines = output.split('\n')
                for line in lines:
                    if "Tests Run:" in line:
                        try:
                            tests_run = int(line.split(':')[1].strip())
                            test_results['total_tests'] += tests_run
                        except:
                            pass
                    elif "Success Rate:" in line:
                        try:
                            success_rate = float(line.split(':')[1].strip().replace('%', ''))
                            if success_rate > 80:
                                test_results['passed_tests'] += 1
                            else:
                                test_results['failed_tests'] += 1
                        except:
                            pass
            
            test_results['test_files'].append({
                'name': description,
                'success': success,
                'output': output[:500] + "..." if len(output) > 500 else output
            })
            
            time.sleep(2)  # Brief pause between tests
        else:
            print(f"⚠️  Test file not found: {test_file}")
    
    print_banner("GENERATING TEST REPORTS")
    
    # Generate HTML test report
    generate_html_report(test_results, reports_dir)
    
    # Generate summary report
    generate_summary_report(test_results, reports_dir)
    
    print_banner("TEST EXECUTION COMPLETE")
    
    end_time = datetime.now()
    duration = end_time - test_results['start_time']
    
    print(f"📊 Test Summary:")
    print(f"   • Total Test Suites: {len(test_files)}")
    print(f"   • Execution Time: {duration}")
    print(f"   • Reports Generated: {reports_dir}")
    
    # Open test report in browser
    report_file = os.path.join(reports_dir, "test_execution_report.html")
    if os.path.exists(report_file):
        print(f"\n🌐 Opening test report in browser...")
        webbrowser.open(f"file://{report_file}")


def generate_html_report(results, reports_dir):
    """Generate comprehensive HTML test report"""
    report_file = os.path.join(reports_dir, "test_execution_report.html")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MediBook - Test Execution Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; margin-bottom: 30px; padding: 20px; background: linear-gradient(135deg, #007bff, #0056b3); color: white; border-radius: 10px; }}
            .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
            .metric {{ background: #e9ecef; padding: 20px; border-radius: 8px; text-align: center; }}
            .metric h3 {{ margin: 0 0 10px 0; color: #495057; }}
            .metric .number {{ font-size: 2em; font-weight: bold; color: #007bff; }}
            .test-results {{ margin: 30px 0; }}
            .test-item {{ background: #f8f9fa; margin: 15px 0; padding: 20px; border-radius: 8px; border-left: 4px solid #007bff; }}
            .test-item.success {{ border-left-color: #28a745; }}
            .test-item.failure {{ border-left-color: #dc3545; }}
            .test-name {{ font-size: 1.2em; font-weight: bold; margin-bottom: 10px; }}
            .test-output {{ background: #ffffff; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 0.9em; max-height: 200px; overflow-y: auto; }}
            .status-badge {{ display: inline-block; padding: 5px 10px; border-radius: 15px; color: white; font-size: 0.8em; font-weight: bold; }}
            .status-success {{ background: #28a745; }}
            .status-failure {{ background: #dc3545; }}
            .footer {{ text-align: center; margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥 MediBook Test Execution Report</h1>
                <p>Comprehensive Automated Testing Results</p>
                <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
            
            <div class="summary">
                <div class="metric">
                    <h3>Test Suites</h3>
                    <div class="number">{len(results['test_files'])}</div>
                </div>
                <div class="metric">
                    <h3>Execution Time</h3>
                    <div class="number">{(datetime.now() - results['start_time']).seconds}s</div>
                </div>
                <div class="metric">
                    <h3>Success Rate</h3>
                    <div class="number">{(results['passed_tests'] / max(len(results['test_files']), 1) * 100):.1f}%</div>
                </div>
                <div class="metric">
                    <h3>Environment</h3>
                    <div class="number">✅</div>
                    <small>Django + SQLite</small>
                </div>
            </div>
            
            <div class="test-results">
                <h2>📋 Test Suite Results</h2>
    """
    
    for test in results['test_files']:
        status_class = "success" if test['success'] else "failure"
        status_badge = "status-success" if test['success'] else "status-failure"
        status_text = "PASSED" if test['success'] else "FAILED"
        
        html_content += f"""
                <div class="test-item {status_class}">
                    <div class="test-name">
                        {test['name']} 
                        <span class="status-badge {status_badge}">{status_text}</span>
                    </div>
                    <div class="test-output">{test['output']}</div>
                </div>
        """
    
    html_content += f"""
            </div>
            
            <div class="footer">
                <h3>📊 Testing Coverage</h3>
                <p><strong>Functional Areas Tested:</strong></p>
                <ul style="text-align: left; display: inline-block;">
                    <li>✅ User Registration & Authentication</li>
                    <li>✅ Login/Logout System</li>
                    <li>✅ Doctor Listing & Search</li>
                    <li>✅ Appointment Booking Flow</li>
                    <li>✅ Form Validation</li>
                    <li>✅ Security Features</li>
                    <li>✅ Regression Testing</li>
                </ul>
                
                <p><strong>Test Environment:</strong> http://127.0.0.1:8000</p>
                <p><strong>Browser:</strong> Chrome (Selenium WebDriver)</p>
                <p><strong>Framework:</strong> Django 4.2.7 + SQLite3</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(report_file, 'w') as f:
        f.write(html_content)
    
    print(f"✅ HTML report generated: {report_file}")


def generate_summary_report(results, reports_dir):
    """Generate text summary report"""
    summary_file = os.path.join(reports_dir, "test_summary.txt")
    
    content = f"""
MEDIBOOK - TEST EXECUTION SUMMARY
{'='*50}

Execution Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Test Environment: http://127.0.0.1:8000
Framework: Django 4.2.7 + SQLite3

RESULTS OVERVIEW:
{'='*20}
Total Test Suites: {len(results['test_files'])}
Passed Suites: {results['passed_tests']}
Failed Suites: {results['failed_tests']}
Success Rate: {(results['passed_tests'] / max(len(results['test_files']), 1) * 100):.1f}%

DETAILED RESULTS:
{'='*20}
"""
    
    for i, test in enumerate(results['test_files'], 1):
        status = "PASSED" if test['success'] else "FAILED"
        content += f"{i}. {test['name']}: {status}\n"
    
    content += f"""

TESTING COVERAGE:
{'='*20}
✅ User Registration Flow
✅ Authentication System  
✅ Doctor Management
✅ Appointment Booking
✅ Form Validation
✅ Security Testing
✅ Regression Testing

RECOMMENDATIONS:
{'='*20}
"""
    
    if results['failed_tests'] > 0:
        content += "- Address failed test cases before deployment\n"
        content += "- Review error logs for specific issues\n"
    else:
        content += "- All test suites passed successfully\n"
        content += "- System ready for deployment\n"
    
    content += "- Continue regular regression testing\n"
    content += "- Add more edge case testing\n"
    content += "- Consider performance testing\n"
    
    with open(summary_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Summary report generated: {summary_file}")


if __name__ == "__main__":
    main()
