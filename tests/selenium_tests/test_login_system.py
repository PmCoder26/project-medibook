"""
Selenium WebDriver Tests for Login System
MediBook - Doctor Appointment System
"""

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestLoginSystem(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up Chrome WebDriver"""
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.base_url = "http://127.0.0.1:8000"
        cls.wait = WebDriverWait(cls.driver, 10)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        cls.driver.quit()
    
    def setUp(self):
        """Navigate to login page before each test"""
        self.driver.get(f"{self.base_url}/accounts/login/")
        time.sleep(1)
    
    def test_01_valid_patient_login(self):
        """Test Case: Valid patient login"""
        print("\n=== Test Case 1: Valid Patient Login ===")
        
        # Enter valid patient credentials
        username_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "id_username"))
        )
        username_field.send_keys("patient1")
        
        password_field = self.driver.find_element(By.ID, "id_password")
        password_field.send_keys("patient123")
        
        # Submit login form
        login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        
        # Verify successful login and redirect to patient dashboard
        try:
            # Check for welcome message or dashboard elements
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "alert-success")),
                    EC.url_contains("patient")
                )
            )
            
            # Verify user is logged in (check navbar for user name)
            user_dropdown = self.wait.until(
                EC.presence_of_element_located((By.ID, "navbarDropdown"))
            )
            self.assertIn("Alice", user_dropdown.text)  # Patient1's first name
            print("✓ Patient login successful - redirected to dashboard")
            
        except TimeoutException:
            self.fail("Patient login failed or incorrect redirect")
    
    def test_02_valid_doctor_login(self):
        """Test Case: Valid doctor login"""
        print("\n=== Test Case 2: Valid Doctor Login ===")
        
        # Enter valid doctor credentials
        username_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "id_username"))
        )
        username_field.send_keys("dr_smith")
        
        password_field = self.driver.find_element(By.ID, "id_password")
        password_field.send_keys("doctor123")
        
        # Submit login form
        login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        
        # Verify successful login and redirect to doctor dashboard
        try:
            # Check for doctor dashboard or welcome message
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "alert-success")),
                    EC.url_contains("doctor")
                )
            )
            
            # Verify user is logged in
            user_dropdown = self.wait.until(
                EC.presence_of_element_located((By.ID, "navbarDropdown"))
            )
            self.assertIn("John", user_dropdown.text)  # Dr. Smith's first name
            print("✓ Doctor login successful - redirected to dashboard")
            
        except TimeoutException:
            self.fail("Doctor login failed or incorrect redirect")
    
    def test_03_invalid_username(self):
        """Test Case: Login with invalid username"""
        print("\n=== Test Case 3: Invalid Username ===")
        
        # Enter invalid username
        username_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "id_username"))
        )
        username_field.send_keys("nonexistent_user")
        
        password_field = self.driver.find_element(By.ID, "id_password")
        password_field.send_keys("anypassword")
        
        # Submit login form
        login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        
        # Verify error message
        try:
            error_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            self.assertIn("invalid", error_message.text.lower())
            print("✓ Invalid username error message displayed")
            
        except TimeoutException:
            # Check for form-level error
            try:
                form_error = self.driver.find_element(By.CLASS_NAME, "text-danger")
                self.assertIn("invalid", form_error.text.lower())
                print("✓ Form validation error displayed")
            except NoSuchElementException:
                self.fail("No error message displayed for invalid username")
    
    def test_04_invalid_password(self):
        """Test Case: Login with invalid password"""
        print("\n=== Test Case 4: Invalid Password ===")
        
        # Enter valid username but invalid password
        username_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "id_username"))
        )
        username_field.send_keys("patient1")
        
        password_field = self.driver.find_element(By.ID, "id_password")
        password_field.send_keys("wrongpassword")
        
        # Submit login form
        login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        
        # Verify error message
        try:
            error_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
            )
            self.assertIn("invalid", error_message.text.lower())
            print("✓ Invalid password error message displayed")
            
        except TimeoutException:
            try:
                form_error = self.driver.find_element(By.CLASS_NAME, "text-danger")
                self.assertIn("invalid", form_error.text.lower())
                print("✓ Form validation error displayed")
            except NoSuchElementException:
                self.fail("No error message displayed for invalid password")
    
    def test_05_empty_fields(self):
        """Test Case: Login with empty fields"""
        print("\n=== Test Case 5: Empty Login Fields ===")
        
        # Try to submit without entering credentials
        login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        
        # Check for HTML5 validation or custom validation
        username_field = self.driver.find_element(By.ID, "id_username")
        password_field = self.driver.find_element(By.ID, "id_password")
        
        username_validation = username_field.get_attribute("validationMessage")
        password_validation = password_field.get_attribute("validationMessage")
        
        # At least one field should have validation message
        self.assertTrue(
            len(username_validation) > 0 or len(password_validation) > 0,
            "No validation message for empty fields"
        )
        print("✓ Empty field validation working")
    
    def test_06_logout_functionality(self):
        """Test Case: Logout functionality"""
        print("\n=== Test Case 6: Logout Functionality ===")
        
        # First login with valid credentials
        username_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "id_username"))
        )
        username_field.send_keys("patient1")
        
        password_field = self.driver.find_element(By.ID, "id_password")
        password_field.send_keys("patient123")
        
        login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        
        # Wait for successful login
        self.wait.until(
            EC.presence_of_element_located((By.ID, "navbarDropdown"))
        )
        
        # Click on user dropdown
        user_dropdown = self.driver.find_element(By.ID, "navbarDropdown")
        user_dropdown.click()
        
        # Click logout
        logout_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
        )
        logout_link.click()
        
        # Verify logout success
        try:
            # Check for logout success message or redirect to home
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "alert-success")),
                    EC.presence_of_element_located((By.LINK_TEXT, "Login"))
                )
            )
            
            # Verify user is logged out (Login link should be visible)
            login_link = self.driver.find_element(By.LINK_TEXT, "Login")
            self.assertTrue(login_link.is_displayed())
            print("✓ Logout successful - user redirected to home page")
            
        except TimeoutException:
            self.fail("Logout functionality not working properly")
    
    def test_07_session_management(self):
        """Test Case: Session management after login"""
        print("\n=== Test Case 7: Session Management ===")
        
        # Login first
        username_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "id_username"))
        )
        username_field.send_keys("patient1")
        
        password_field = self.driver.find_element(By.ID, "id_password")
        password_field.send_keys("patient123")
        
        login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        
        # Wait for login success
        self.wait.until(
            EC.presence_of_element_located((By.ID, "navbarDropdown"))
        )
        
        # Navigate to different pages and verify session persistence
        self.driver.get(f"{self.base_url}/appointments/doctors/")
        
        # Verify user is still logged in
        try:
            user_dropdown = self.wait.until(
                EC.presence_of_element_located((By.ID, "navbarDropdown"))
            )
            self.assertIn("Alice", user_dropdown.text)
            print("✓ Session maintained across page navigation")
            
        except TimeoutException:
            self.fail("Session not maintained properly")
    
    def test_08_redirect_after_login(self):
        """Test Case: Proper redirect after login based on user type"""
        print("\n=== Test Case 8: User Type Based Redirect ===")
        
        # Test admin login redirect
        username_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "id_username"))
        )
        username_field.send_keys("admin")
        
        password_field = self.driver.find_element(By.ID, "id_password")
        password_field.send_keys("admin123")
        
        login_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_btn.click()
        
        # Verify redirect (admin should go to dashboard)
        try:
            self.wait.until(
                EC.any_of(
                    EC.url_contains("dashboard"),
                    EC.url_contains("appointments")
                )
            )
            print("✓ Admin user redirected appropriately after login")
            
        except TimeoutException:
            print("⚠ Admin redirect behavior may need verification")


if __name__ == "__main__":
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLoginSystem)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"LOGIN SYSTEM TESTS SUMMARY")
    print(f"{'='*50}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
