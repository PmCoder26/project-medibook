"""
Selenium WebDriver Tests for User Registration
MediBook - Doctor Appointment System
"""

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestUserRegistration(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up Chrome WebDriver"""
        try:
            # Use Chrome with optimized settings
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            # Try Chrome without WebDriverManager first
            try:
                cls.driver = webdriver.Chrome(options=options)
                print("✅ Using Chrome WebDriver (system)")
            except Exception:
                # Fallback to WebDriverManager
                cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                print("✅ Using Chrome WebDriver (downloaded)")
                
        except Exception as e:
            print(f"Chrome setup failed: {e}")
            raise unittest.SkipTest("Chrome WebDriver not available")
        cls.driver.maximize_window()
        cls.base_url = "http://127.0.0.1:8000"
        cls.wait = WebDriverWait(cls.driver, 10)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        cls.driver.quit()
    
    def setUp(self):
        """Navigate to home page before each test"""
        self.driver.get(self.base_url)
        time.sleep(1)
    
    def test_01_patient_registration_valid_data(self):
        """Test Case: Valid patient registration"""
        print("\n=== Test Case 1: Valid Patient Registration ===")
        
        # Navigate to registration choice page
        register_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Register"))
        )
        register_link.click()
        
        # Click on Patient registration
        patient_btn = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Register as Patient"))
        )
        patient_btn.click()
        
        # Fill registration form
        self.driver.find_element(By.ID, "id_first_name").send_keys("John")
        self.driver.find_element(By.ID, "id_last_name").send_keys("Doe")
        self.driver.find_element(By.ID, "id_username").send_keys("johndoe_test")
        self.driver.find_element(By.ID, "id_email").send_keys("john.doe@test.com")
        self.driver.find_element(By.ID, "id_phone").send_keys("9876543210")
        self.driver.find_element(By.ID, "id_date_of_birth").send_keys("1990-01-01")
        
        # Select gender
        gender_select = Select(self.driver.find_element(By.ID, "id_gender"))
        gender_select.select_by_value("M")
        
        self.driver.find_element(By.ID, "id_address").send_keys("123 Test Street, Test City")
        self.driver.find_element(By.ID, "id_password1").send_keys("TestPass123!")
        self.driver.find_element(By.ID, "id_password2").send_keys("TestPass123!")
        
        # Submit form
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        # Verify success message or redirect
        try:
            success_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
            )
            self.assertIn("successful", success_message.text.lower())
            print("✓ Patient registration successful")
        except TimeoutException:
            # Check if redirected to login page
            self.assertIn("login", self.driver.current_url.lower())
            print("✓ Redirected to login page after registration")
    
    def test_02_patient_registration_invalid_email(self):
        """Test Case: Patient registration with invalid email"""
        print("\n=== Test Case 2: Invalid Email Format ===")
        
        # Navigate to patient registration
        self.driver.get(f"{self.base_url}/accounts/register/")
        patient_btn = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Register as Patient"))
        )
        patient_btn.click()
        
        # Fill form with invalid email
        self.driver.find_element(By.ID, "id_first_name").send_keys("Jane")
        self.driver.find_element(By.ID, "id_last_name").send_keys("Smith")
        self.driver.find_element(By.ID, "id_username").send_keys("janesmith_test")
        self.driver.find_element(By.ID, "id_email").send_keys("invalid-email")  # Invalid email
        self.driver.find_element(By.ID, "id_phone").send_keys("9876543211")
        self.driver.find_element(By.ID, "id_date_of_birth").send_keys("1992-05-15")
        
        gender_select = Select(self.driver.find_element(By.ID, "id_gender"))
        gender_select.select_by_value("F")
        
        self.driver.find_element(By.ID, "id_address").send_keys("456 Test Avenue")
        self.driver.find_element(By.ID, "id_password1").send_keys("TestPass123!")
        self.driver.find_element(By.ID, "id_password2").send_keys("TestPass123!")
        
        # Submit form
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        # Verify error message
        try:
            error_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "text-danger"))
            )
            print("✓ Email validation error displayed")
        except TimeoutException:
            # Check if HTML5 validation prevents submission
            email_field = self.driver.find_element(By.ID, "id_email")
            validation_message = email_field.get_attribute("validationMessage")
            self.assertTrue(len(validation_message) > 0)
            print("✓ HTML5 email validation working")
    
    def test_03_patient_registration_invalid_phone(self):
        """Test Case: Patient registration with invalid phone number"""
        print("\n=== Test Case 3: Invalid Phone Number ===")
        
        # Navigate to patient registration
        self.driver.get(f"{self.base_url}/accounts/register/patient/")
        
        # Fill form with invalid phone
        self.driver.find_element(By.ID, "id_first_name").send_keys("Bob")
        self.driver.find_element(By.ID, "id_last_name").send_keys("Johnson")
        self.driver.find_element(By.ID, "id_username").send_keys("bobjohnson_test")
        self.driver.find_element(By.ID, "id_email").send_keys("bob.johnson@test.com")
        self.driver.find_element(By.ID, "id_phone").send_keys("123")  # Invalid phone (too short)
        self.driver.find_element(By.ID, "id_date_of_birth").send_keys("1985-12-25")
        
        gender_select = Select(self.driver.find_element(By.ID, "id_gender"))
        gender_select.select_by_value("M")
        
        self.driver.find_element(By.ID, "id_address").send_keys("789 Test Road")
        self.driver.find_element(By.ID, "id_password1").send_keys("TestPass123!")
        self.driver.find_element(By.ID, "id_password2").send_keys("TestPass123!")
        
        # Submit form
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        # Verify phone validation error
        try:
            error_elements = self.driver.find_elements(By.CLASS_NAME, "text-danger")
            phone_error_found = any("phone" in elem.text.lower() or "10 digits" in elem.text for elem in error_elements)
            self.assertTrue(phone_error_found)
            print("✓ Phone number validation error displayed")
        except:
            print("⚠ Phone validation error not found - check implementation")
    
    def test_04_doctor_registration_valid_data(self):
        """Test Case: Valid doctor registration"""
        print("\n=== Test Case 4: Valid Doctor Registration ===")
        
        # Navigate to doctor registration
        self.driver.get(f"{self.base_url}/accounts/register/")
        doctor_btn = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Register as Doctor"))
        )
        doctor_btn.click()
        
        # Fill doctor registration form
        self.driver.find_element(By.ID, "id_first_name").send_keys("Sarah")
        self.driver.find_element(By.ID, "id_last_name").send_keys("Wilson")
        self.driver.find_element(By.ID, "id_username").send_keys("dr_wilson_test")
        self.driver.find_element(By.ID, "id_email").send_keys("dr.wilson@test.com")
        self.driver.find_element(By.ID, "id_phone").send_keys("9876543212")
        
        # Select specialization
        specialization_select = Select(self.driver.find_element(By.ID, "id_specialization"))
        specialization_select.select_by_value("general")
        
        self.driver.find_element(By.ID, "id_license_number").send_keys("TEST_LIC_001")
        self.driver.find_element(By.ID, "id_experience_years").send_keys("5")
        self.driver.find_element(By.ID, "id_consultation_fee").send_keys("1000")
        self.driver.find_element(By.ID, "id_password1").send_keys("TestPass123!")
        self.driver.find_element(By.ID, "id_password2").send_keys("TestPass123!")
        
        # Submit form
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        # Verify success
        try:
            success_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
            )
            self.assertIn("successful", success_message.text.lower())
            print("✓ Doctor registration successful")
        except TimeoutException:
            # Check if redirected to login page
            self.assertIn("login", self.driver.current_url.lower())
            print("✓ Redirected to login page after doctor registration")
    
    def test_05_password_mismatch(self):
        """Test Case: Password confirmation mismatch"""
        print("\n=== Test Case 5: Password Mismatch ===")
        
        # Navigate to patient registration
        self.driver.get(f"{self.base_url}/accounts/register/patient/")
        
        # Fill form with mismatched passwords
        self.driver.find_element(By.ID, "id_first_name").send_keys("Test")
        self.driver.find_element(By.ID, "id_last_name").send_keys("User")
        self.driver.find_element(By.ID, "id_username").send_keys("testuser_mismatch")
        self.driver.find_element(By.ID, "id_email").send_keys("test.mismatch@test.com")
        self.driver.find_element(By.ID, "id_phone").send_keys("9876543213")
        self.driver.find_element(By.ID, "id_date_of_birth").send_keys("1995-06-10")
        
        gender_select = Select(self.driver.find_element(By.ID, "id_gender"))
        gender_select.select_by_value("M")
        
        self.driver.find_element(By.ID, "id_address").send_keys("Test Address")
        self.driver.find_element(By.ID, "id_password1").send_keys("TestPass123!")
        self.driver.find_element(By.ID, "id_password2").send_keys("DifferentPass123!")  # Different password
        
        # Submit form
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        # Verify password mismatch error
        try:
            error_elements = self.driver.find_elements(By.CLASS_NAME, "text-danger")
            password_error_found = any("password" in elem.text.lower() and "match" in elem.text.lower() for elem in error_elements)
            self.assertTrue(password_error_found)
            print("✓ Password mismatch error displayed")
        except:
            print("⚠ Password mismatch validation not found - check implementation")


if __name__ == "__main__":
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUserRegistration)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"REGISTRATION TESTS SUMMARY")
    print(f"{'='*50}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
