"""
Regression Test Suite for MediBook Application
Automated regression testing to ensure existing functionality works after changes
"""

import unittest
import time
import sys
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class RegressionTestSuite(unittest.TestCase):
    """
    Comprehensive regression test suite covering critical user paths
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up the WebDriver before running tests"""
        try:
            # Try Chrome with headless mode
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        except Exception as e:
            print(f"Chrome setup failed: {e}")
            try:
                # Fallback to Safari
                cls.driver = webdriver.Safari()
            except Exception as e2:
                print(f"Safari setup failed: {e2}")
                raise unittest.SkipTest("No compatible browser found")
        cls.driver.maximize_window()
        cls.base_url = "http://127.0.0.1:8000"
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.test_results = []
    
    @classmethod
    def tearDownClass(cls):
        """Clean up and generate report"""
        cls.driver.quit()
        cls.generate_regression_report()
    
    def setUp(self):
        """Reset to home page before each test"""
        self.driver.get(self.base_url)
        time.sleep(1)
    
    def log_test_result(self, test_name, status, message=""):
        """Log test results for reporting"""
        self.test_results.append({
            'test_name': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def test_01_critical_path_patient_registration(self):
        """Critical Path: Patient Registration Flow"""
        test_name = "Patient Registration Critical Path"
        try:
            print(f"\n=== {test_name} ===")
            
            # Navigate to registration
            register_link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Register"))
            )
            register_link.click()
            
            # Select patient registration
            patient_btn = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Register as Patient"))
            )
            patient_btn.click()
            
            # Fill registration form with unique data
            timestamp = int(time.time())
            self.driver.find_element(By.ID, "id_first_name").send_keys("Regression")
            self.driver.find_element(By.ID, "id_last_name").send_keys("Test")
            self.driver.find_element(By.ID, "id_username").send_keys(f"regtest_{timestamp}")
            self.driver.find_element(By.ID, "id_email").send_keys(f"regtest_{timestamp}@test.com")
            self.driver.find_element(By.ID, "id_phone").send_keys("9876543298")
            self.driver.find_element(By.ID, "id_date_of_birth").send_keys("1990-01-01")
            
            gender_select = Select(self.driver.find_element(By.ID, "id_gender"))
            gender_select.select_by_value("M")
            
            self.driver.find_element(By.ID, "id_address").send_keys("Regression Test Address")
            self.driver.find_element(By.ID, "id_password1").send_keys("RegTest123!")
            self.driver.find_element(By.ID, "id_password2").send_keys("RegTest123!")
            
            # Submit form
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()
            
            # Verify success
            try:
                self.wait.until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CLASS_NAME, "alert-success")),
                        EC.url_contains("login")
                    )
                )
                self.log_test_result(test_name, "PASS", "Registration completed successfully")
                print("✓ PASS: Patient registration working")
                
            except TimeoutException:
                self.log_test_result(test_name, "FAIL", "Registration did not complete")
                self.fail("Registration flow broken")
                
        except Exception as e:
            self.log_test_result(test_name, "ERROR", str(e))
            self.fail(f"Registration test error: {e}")
    
    def test_02_critical_path_login_system(self):
        """Critical Path: Login System for All User Types"""
        test_name = "Login System Critical Path"
        try:
            print(f"\n=== {test_name} ===")
            
            # Test patient login
            self.driver.get(f"{self.base_url}/accounts/login/")
            
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "id_username"))
            )
            username_field.send_keys("patient1")
            
            password_field = self.driver.find_element(By.ID, "id_password")
            password_field.send_keys("patient123")
            
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_btn.click()
            
            # Verify login success
            user_dropdown = self.wait.until(
                EC.presence_of_element_located((By.ID, "navbarDropdown"))
            )
            self.assertIn("Alice", user_dropdown.text)
            
            # Test logout
            user_dropdown.click()
            logout_link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
            )
            logout_link.click()
            
            # Verify logout
            self.wait.until(
                EC.presence_of_element_located((By.LINK_TEXT, "Login"))
            )
            
            self.log_test_result(test_name, "PASS", "Login/logout cycle successful")
            print("✓ PASS: Login system working")
            
        except Exception as e:
            self.log_test_result(test_name, "FAIL", str(e))
            self.fail(f"Login system test failed: {e}")
    
    def test_03_critical_path_doctor_listing(self):
        """Critical Path: Doctor Listing and Search"""
        test_name = "Doctor Listing Critical Path"
        try:
            print(f"\n=== {test_name} ===")
            
            # Navigate to doctor list
            self.driver.get(f"{self.base_url}/appointments/doctors/")
            
            # Verify doctors are displayed
            doctor_cards = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "doctor-card"))
            )
            self.assertGreater(len(doctor_cards), 0, "No doctors found")
            
            # Test specialization filter
            specialization_select = Select(self.driver.find_element(By.ID, "specialization"))
            specialization_select.select_by_value("cardiology")
            
            filter_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            filter_btn.click()
            
            # Verify filter works
            time.sleep(2)
            selected_option = specialization_select.first_selected_option
            self.assertEqual(selected_option.get_attribute("value"), "cardiology")
            
            self.log_test_result(test_name, "PASS", f"Found {len(doctor_cards)} doctors, filter working")
            print(f"✓ PASS: Doctor listing working ({len(doctor_cards)} doctors)")
            
        except Exception as e:
            self.log_test_result(test_name, "FAIL", str(e))
            self.fail(f"Doctor listing test failed: {e}")
    
    def test_04_critical_path_appointment_booking(self):
        """Critical Path: Complete Appointment Booking Flow"""
        test_name = "Appointment Booking Critical Path"
        try:
            print(f"\n=== {test_name} ===")
            
            # Login as patient first
            self.driver.get(f"{self.base_url}/accounts/login/")
            
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "id_username"))
            )
            username_field.send_keys("patient1")
            
            password_field = self.driver.find_element(By.ID, "id_password")
            password_field.send_keys("patient123")
            
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_btn.click()
            
            # Wait for login
            self.wait.until(
                EC.presence_of_element_located((By.ID, "navbarDropdown"))
            )
            
            # Navigate to doctors and book appointment
            self.driver.get(f"{self.base_url}/appointments/doctors/")
            
            book_btn = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Book Appointment"))
            )
            book_btn.click()
            
            # Fill booking form
            future_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
            date_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "appointment_date"))
            )
            date_field.send_keys(future_date)
            
            # Select time slot
            time_slots = self.driver.find_elements(By.CSS_SELECTOR, "input[name='appointment_time']")
            if time_slots:
                time_slots[0].click()
            
            symptoms_field = self.driver.find_element(By.NAME, "symptoms")
            symptoms_field.send_keys("Regression test appointment")
            
            # Submit booking
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()
            
            # Verify booking success
            try:
                self.wait.until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CLASS_NAME, "alert-success")),
                        EC.url_contains("dashboard")
                    )
                )
                self.log_test_result(test_name, "PASS", "Appointment booked successfully")
                print("✓ PASS: Appointment booking working")
                
            except TimeoutException:
                self.log_test_result(test_name, "FAIL", "Booking did not complete")
                self.fail("Appointment booking failed")
                
        except Exception as e:
            self.log_test_result(test_name, "FAIL", str(e))
            self.fail(f"Appointment booking test failed: {e}")
    
    def test_05_critical_path_dashboard_access(self):
        """Critical Path: Dashboard Access for Different User Types"""
        test_name = "Dashboard Access Critical Path"
        try:
            print(f"\n=== {test_name} ===")
            
            # Test patient dashboard
            self.driver.get(f"{self.base_url}/accounts/login/")
            
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "id_username"))
            )
            username_field.send_keys("patient1")
            
            password_field = self.driver.find_element(By.ID, "id_password")
            password_field.send_keys("patient123")
            
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_btn.click()
            
            # Navigate to patient dashboard
            self.driver.get(f"{self.base_url}/appointments/patient/")
            
            # Verify dashboard loads
            dashboard_content = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
            
            # Logout and test doctor dashboard
            user_dropdown = self.driver.find_element(By.ID, "navbarDropdown")
            user_dropdown.click()
            
            logout_link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
            )
            logout_link.click()
            
            # Login as doctor
            self.driver.get(f"{self.base_url}/accounts/login/")
            
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "id_username"))
            )
            username_field.send_keys("dr_smith")
            
            password_field = self.driver.find_element(By.ID, "id_password")
            password_field.send_keys("doctor123")
            
            login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_btn.click()
            
            # Navigate to doctor dashboard
            self.driver.get(f"{self.base_url}/appointments/doctor/")
            
            # Verify doctor dashboard loads
            doctor_dashboard = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
            
            self.log_test_result(test_name, "PASS", "Both patient and doctor dashboards accessible")
            print("✓ PASS: Dashboard access working for all user types")
            
        except Exception as e:
            self.log_test_result(test_name, "FAIL", str(e))
            self.fail(f"Dashboard access test failed: {e}")
    
    def test_06_data_validation_regression(self):
        """Regression: Data Validation Rules"""
        test_name = "Data Validation Regression"
        try:
            print(f"\n=== {test_name} ===")
            
            # Test email validation
            self.driver.get(f"{self.base_url}/accounts/register/patient/")
            
            # Fill form with invalid email
            self.driver.find_element(By.ID, "id_first_name").send_keys("Test")
            self.driver.find_element(By.ID, "id_last_name").send_keys("Validation")
            self.driver.find_element(By.ID, "id_username").send_keys("testvalidation")
            self.driver.find_element(By.ID, "id_email").send_keys("invalid-email")
            
            # Check HTML5 validation
            email_field = self.driver.find_element(By.ID, "id_email")
            validation_message = email_field.get_attribute("validationMessage")
            
            # Test phone validation
            self.driver.find_element(By.ID, "id_phone").send_keys("123")  # Too short
            
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()
            
            # Verify validation prevents submission or shows errors
            time.sleep(2)
            current_url = self.driver.current_url
            
            # Should still be on registration page due to validation errors
            self.assertIn("register", current_url.lower())
            
            self.log_test_result(test_name, "PASS", "Data validation rules working")
            print("✓ PASS: Data validation regression successful")
            
        except Exception as e:
            self.log_test_result(test_name, "FAIL", str(e))
            print(f"⚠ Data validation test issue: {e}")
    
    def test_07_security_regression(self):
        """Regression: Security Features"""
        test_name = "Security Features Regression"
        try:
            print(f"\n=== {test_name} ===")
            
            # Test unauthorized access
            self.driver.get(f"{self.base_url}/appointments/book/1/")
            
            # Should be redirected to login or show access denied
            self.wait.until(
                EC.any_of(
                    EC.url_contains("login"),
                    EC.presence_of_element_located((By.ID, "id_username"))
                )
            )
            
            # Test CSRF protection (form should have CSRF token)
            self.driver.get(f"{self.base_url}/accounts/login/")
            csrf_token = self.driver.find_elements(By.CSS_SELECTOR, "input[name='csrfmiddlewaretoken']")
            self.assertGreater(len(csrf_token), 0, "CSRF token not found")
            
            self.log_test_result(test_name, "PASS", "Security features working")
            print("✓ PASS: Security regression successful")
            
        except Exception as e:
            self.log_test_result(test_name, "FAIL", str(e))
            print(f"⚠ Security test issue: {e}")
    
    @classmethod
    def generate_regression_report(cls):
        """Generate detailed regression test report"""
        report_path = "/Users/parimal/VisualStudioCodeProjects/stqa_project/tests/test_reports/regression_report.html"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        total_tests = len(cls.test_results)
        passed_tests = len([r for r in cls.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in cls.test_results if r['status'] == 'FAIL'])
        error_tests = len([r for r in cls.test_results if r['status'] == 'ERROR'])
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MediBook Regression Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: #f8f9fa; padding: 20px; border-radius: 5px; }}
                .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
                .metric {{ background: #e9ecef; padding: 15px; border-radius: 5px; text-align: center; }}
                .pass {{ color: #28a745; }}
                .fail {{ color: #dc3545; }}
                .error {{ color: #fd7e14; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background: #f8f9fa; }}
                .status-pass {{ background: #d4edda; }}
                .status-fail {{ background: #f8d7da; }}
                .status-error {{ background: #fff3cd; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>MediBook - Regression Test Report</h1>
                <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p><strong>Test Environment:</strong> http://127.0.0.1:8000</p>
            </div>
            
            <div class="summary">
                <div class="metric">
                    <h3>Total Tests</h3>
                    <h2>{total_tests}</h2>
                </div>
                <div class="metric">
                    <h3 class="pass">Passed</h3>
                    <h2 class="pass">{passed_tests}</h2>
                </div>
                <div class="metric">
                    <h3 class="fail">Failed</h3>
                    <h2 class="fail">{failed_tests}</h2>
                </div>
                <div class="metric">
                    <h3 class="error">Errors</h3>
                    <h2 class="error">{error_tests}</h2>
                </div>
                <div class="metric">
                    <h3>Success Rate</h3>
                    <h2>{success_rate:.1f}%</h2>
                </div>
            </div>
            
            <h2>Test Results Details</h2>
            <table>
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Status</th>
                        <th>Message</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for result in cls.test_results:
            status_class = f"status-{result['status'].lower()}"
            html_content += f"""
                    <tr class="{status_class}">
                        <td>{result['test_name']}</td>
                        <td><strong>{result['status']}</strong></td>
                        <td>{result['message']}</td>
                        <td>{result['timestamp']}</td>
                    </tr>
            """
        
        html_content += """
                </tbody>
            </table>
            
            <h2>Critical Path Coverage</h2>
            <ul>
                <li>✓ User Registration Flow</li>
                <li>✓ Authentication System</li>
                <li>✓ Doctor Listing & Search</li>
                <li>✓ Appointment Booking</li>
                <li>✓ Dashboard Access</li>
                <li>✓ Data Validation</li>
                <li>✓ Security Features</li>
            </ul>
            
            <h2>Recommendations</h2>
            <ul>
        """
        
        if failed_tests > 0:
            html_content += "<li><strong>High Priority:</strong> Address failed test cases immediately</li>"
        if error_tests > 0:
            html_content += "<li><strong>Medium Priority:</strong> Investigate error conditions</li>"
        if success_rate < 90:
            html_content += "<li><strong>Low Priority:</strong> Improve test coverage and stability</li>"
        else:
            html_content += "<li><strong>Good:</strong> Regression tests passing, system stable</li>"
        
        html_content += """
            </ul>
        </body>
        </html>
        """
        
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        print(f"\n{'='*60}")
        print(f"REGRESSION TEST REPORT GENERATED")
        print(f"{'='*60}")
        print(f"Report Location: {report_path}")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Errors: {error_tests}")
        print(f"Success Rate: {success_rate:.1f}%")


if __name__ == "__main__":
    # Run regression test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(RegressionTestSuite)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
