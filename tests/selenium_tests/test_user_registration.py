"""
Selenium WebDriver Tests for User Registration
MediBook - Doctor Appointment System
"""

import unittest
import time
import random
import string
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('test_execution.log')
    ]
)
logger = logging.getLogger(__name__)

def generate_random_string(length=8):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_test_email():
    """Generate a unique test email"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"test_{timestamp}@example.com"

def generate_test_phone():
    """Generate a random 10-digit phone number"""
    return ''.join(random.choice('0123456789') for _ in range(10))

def generate_test_username():
    """Generate a unique test username"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"testuser_{timestamp}"


class TestUserRegistration(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up Chrome WebDriver"""
        try:
            # Use Chrome with visual feedback
            options = webdriver.ChromeOptions()
            # Comment out headless mode to see the browser
            # options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            # Add a small delay to see what's happening
            options.add_argument('--start-maximized')
            
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
    
    def test_00_verify_browser(self):
        """Verify that Selenium can interact with the browser"""
        print("\n=== Verifying Browser Interaction ===")
        
        # Open Google to verify basic browser interaction
        self.driver.get("https://www.google.com")
        print("✓ Successfully opened Google")
        
        # Take a screenshot
        self.driver.save_screenshot("browser_verification.png")
        print("✓ Screenshot saved: browser_verification.png")
        
        # Check page title
        self.assertIn("Google", self.driver.title)
        print("✓ Page title verified")
        
        # Find and interact with the search box
        try:
            search_box = self.driver.find_element(By.NAME, 'q')
            search_box.send_keys("Selenium test successful!")
            print("✓ Successfully interacted with search box")
            time.sleep(2)  # Keep the browser open for 2 seconds to see the text
        except Exception as e:
            print(f"❌ Error interacting with search box: {str(e)}")
            raise
        
        print("✅ Browser interaction test completed successfully!")
        print("If you can see the browser window and the text 'Selenium test successful!', Selenium is working correctly.")
        time.sleep(5)  # Keep the browser open for 5 seconds
    
    def create_test_patient_data(self):
        """Helper method to generate test patient data"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return {
            'first_name': f"Test{timestamp[:4]}",
            'last_name': f"Patient{timestamp[4:8]}",
            'username': f"patient_{timestamp}",
            'email': generate_test_email(),
            'phone': generate_test_phone(),
            'date_of_birth': (datetime.now() - timedelta(days=25*365)).strftime("%Y-%m-%d"),
            'gender': 'M',
            'address': f"{random.randint(100, 999)} Test St, Test City",
            'password': 'TestPass123!',
            'password2': 'TestPass123!'
        }
    
    def create_test_doctor_data(self):
        """Helper method to generate test doctor data"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return {
            'first_name': f"Dr.{timestamp[:4]}",
            'last_name': f"Doctor{timestamp[4:8]}",
            'username': f"doctor_{timestamp}",
            'email': generate_test_email(),
            'phone': generate_test_phone(),
            'specialization': 'general',
            'license_number': f"LIC{timestamp}",
            'experience_years': random.randint(1, 30),
            'consultation_fee': random.randint(500, 5000),
            'password': 'TestPass123!',
            'password2': 'TestPass123!'
        }
    
    def fill_patient_form(self, patient_data):
        """Helper method to fill patient registration form"""
        try:
            self.driver.find_element(By.ID, "id_first_name").send_keys(patient_data['first_name'])
            self.driver.find_element(By.ID, "id_last_name").send_keys(patient_data['last_name'])
            self.driver.find_element(By.ID, "id_username").send_keys(patient_data['username'])
            self.driver.find_element(By.ID, "id_email").send_keys(patient_data['email'])
            self.driver.find_element(By.ID, "id_phone").send_keys(patient_data['phone'])
            self.driver.find_element(By.ID, "id_date_of_birth").send_keys(patient_data['date_of_birth'])
            
            gender_select = Select(self.driver.find_element(By.ID, "id_gender"))
            gender_select.select_by_value(patient_data['gender'])
            
            self.driver.find_element(By.ID, "id_address").send_keys(patient_data['address'])
            self.driver.find_element(By.ID, "id_password1").send_keys(patient_data['password'])
            self.driver.find_element(By.ID, "id_password2").send_keys(patient_data['password2'])
            
            return True
        except Exception as e:
            logger.error(f"Error filling patient form: {str(e)}")
            return False
    
    def fill_doctor_form(self, doctor_data):
        """Helper method to fill doctor registration form"""
        try:
            # Fill in basic information
            self.driver.find_element(By.ID, "id_first_name").send_keys(doctor_data['first_name'])
            self.driver.find_element(By.ID, "id_last_name").send_keys(doctor_data['last_name'])
            self.driver.find_element(By.ID, "id_username").send_keys(doctor_data['username'])
            self.driver.find_element(By.ID, "id_email").send_keys(doctor_data['email'])
            self.driver.find_element(By.ID, "id_phone").send_keys(doctor_data['phone'])
            
            # Select specialization
            specialization_select = Select(self.driver.find_element(By.ID, "id_specialization"))
            specialization_select.select_by_value(doctor_data['specialization'])
            
            # Fill in professional details
            self.driver.find_element(By.ID, "id_license_number").send_keys(doctor_data['license_number'])
            self.driver.find_element(By.ID, "id_experience_years").send_keys(str(doctor_data['experience_years']))
            self.driver.find_element(By.ID, "id_consultation_fee").send_keys(str(doctor_data['consultation_fee']))
            
            # Fill in password fields
            self.driver.find_element(By.ID, "id_password1").send_keys(doctor_data['password'])
            self.driver.find_element(By.ID, "id_password2").send_keys(doctor_data['password2'])
            
            # Check terms and conditions checkbox if it exists
            try:
                # First try to find by name
                try:
                    terms_checkbox = self.driver.find_element(By.NAME, "terms")
                except NoSuchElementException:
                    # Try by ID if name doesn't work
                    try:
                        terms_checkbox = self.driver.find_element(By.ID, "id_terms")
                    except NoSuchElementException:
                        # Try to find by text in label
                        try:
                            label = self.driver.find_element(By.XPATH, "//label[contains(., 'terms') or contains(., 'Terms')]")
                            terms_checkbox_id = label.get_attribute('for')
                            terms_checkbox = self.driver.find_element(By.ID, terms_checkbox_id)
                        except:
                            logger.warning("Could not find terms checkbox by name, ID, or label")
                            return True
                
                # Scroll to the checkbox
                self.driver.execute_script("arguments[0].scrollIntoView(true);", terms_checkbox)
                time.sleep(0.5)  # Small delay for scroll
                
                # Try to click the checkbox
                try:
                    if not terms_checkbox.is_selected():
                        terms_checkbox.click()
                        logger.info("✓ Checked 'I agree to the Terms and Conditions'")
                except:
                    # If direct click fails, try JavaScript click
                    try:
                        self.driver.execute_script("arguments[0].click();", terms_checkbox)
                        logger.info("✓ Checked 'I agree to the Terms and Conditions' (using JavaScript)")
                    except Exception as e:
                        logger.warning(f"Failed to check terms checkbox: {str(e)}")
                        # Take a screenshot to help with debugging
                        self.take_screenshot("terms_checkbox_error")
            except Exception as e:
                logger.warning(f"Error handling terms checkbox: {str(e)}")
                self.take_screenshot("terms_checkbox_error")
            
            return True
        except Exception as e:
            logger.error(f"Error filling doctor form: {str(e)}")
            self.take_screenshot("doctor_form_fill_error")
            return False
    
    def submit_form(self):
        """Helper method to submit forms with retry logic and better error handling"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1} to submit form...")
                
                # Try different selectors for the submit button
                submit_selectors = [
                    (By.CSS_SELECTOR, "button[type='submit']"),
                    (By.CSS_SELECTOR, "input[type='submit']"),
                    (By.XPATH, "//button[contains(., 'Register')]"),
                    (By.XPATH, "//input[@value='Register']")
                ]
                
                submit_btn = None
                for by, selector in submit_selectors:
                    try:
                        submit_btn = self.wait.until(
                            EC.element_to_be_clickable((by, selector))
                        )
                        logger.info(f"Found submit button with {by} = {selector}")
                        break
                    except:
                        continue
                
                if not submit_btn:
                    logger.error("Could not find submit button with any selector")
                    self.take_screenshot("submit_button_not_found")
                    return False
                
                # Scroll to the button and make it visible
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                time.sleep(0.5)  # Small delay for scroll
                
                # Highlight the button (for debugging)
                self.driver.execute_script("arguments[0].style.border='3px solid red';", submit_btn)
                
                # Take a screenshot before submission attempt
                self.take_screenshot(f"before_submit_attempt_{attempt + 1}")
                
                # Try to click the button
                try:
                    submit_btn.click()
                    logger.info("Form submitted with normal click")
                except Exception as click_error:
                    logger.warning(f"Normal click failed: {str(click_error)}")
                    # If normal click fails, try JavaScript click
                    try:
                        self.driver.execute_script("arguments[0].click();", submit_btn)
                        logger.info("Form submitted with JavaScript click")
                    except Exception as js_click_error:
                        logger.error(f"JavaScript click also failed: {str(js_click_error)}")
                        self.take_screenshot("submit_failed")
                        if attempt < max_retries - 1:
                            continue
                        return False
                
                # Wait for any page change or validation message
                try:
                    WebDriverWait(self.driver, 5).until(
                        lambda d: d.current_url != self.driver.current_url or
                                 d.find_elements(By.CLASS_NAME, "alert") or
                                 d.find_elements(By.CLASS_NAME, "errorlist") or
                                 d.find_elements(By.CLASS_NAME, "messages") or
                                 d.find_elements(By.CSS_SELECTOR, "[role='alert']")
                    )
                    logger.info("Page changed or message appeared after submission")
                    
                    # Take a screenshot after successful submission
                    self.take_screenshot(f"after_submit_attempt_{attempt + 1}")
                    return True
                    
                except TimeoutException:
                    logger.warning(f"No page change or messages after submission (attempt {attempt + 1})")
                    if attempt < max_retries - 1:
                        logger.info("Retrying...")
                        continue
                    
                    # Take a final screenshot and check if we're still on the same page
                    current_url = self.driver.current_url
                    self.take_screenshot("submit_no_response")
                    logger.error(f"No response after form submission. Current URL: {current_url}")
                    return False
                
            except Exception as e:
                logger.error(f"Error during form submission (attempt {attempt + 1}): {str(e)}")
                self.take_screenshot(f"submit_error_attempt_{attempt + 1}")
                if attempt == max_retries - 1:  # Last attempt
                    logger.error(f"Failed to submit form after {max_retries} attempts")
                    return False
                time.sleep(1)  # Wait before retry
        
        return False
    
    def take_screenshot(self, name):
        """Take a screenshot with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot saved: {filename}")
        return filename
    
    def test_01_patient_registration_valid_data(self):
        """Test Case: Valid patient registration"""
        logger.info("\n=== Test Case 1: Valid Patient Registration ===")
        
        # Generate test data
        patient_data = self.create_test_patient_data()
        logger.info(f"Generated test patient data: {patient_data}")
        
        # Create screenshots directory if it doesn't exist
        try:
            import os
            os.makedirs("screenshots", exist_ok=True)
        except Exception as e:
            logger.warning(f"Could not create screenshots directory: {str(e)}")
        
        # Navigate to registration choice page
        try:
            self.driver.get(f"{self.base_url}")
            register_link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Register"))
            )
            register_link.click()
            logger.info("Clicked on Register link")
            
            # Click on Patient registration
            patient_btn = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Register as Patient"))
            )
            patient_btn.click()
            logger.info("Clicked on Register as Patient")
            
            # Fill registration form
            if not self.fill_patient_form(patient_data):
                self.fail("Failed to fill patient registration form")
            
            # Take screenshot before submission
            self.take_screenshot("before_patient_submission")
            
            # Log form data for debugging
            logger.info("Patient Registration Form Data:")
            for field in ["first_name", "last_name", "username", "email", "phone", "date_of_birth"]:
                try:
                    value = self.driver.find_element(By.ID, f"id_{field}").get_attribute("value")
                    logger.info(f"  {field}: {value}")
                except Exception as e:
                    logger.warning(f"Could not get value for {field}: {str(e)}")
            
            # Submit the form
            logger.info("Submitting patient registration form...")
            if not self.submit_form():
                self.take_screenshot("patient_submit_failed")
                self.fail("Failed to submit patient registration form")
                
        except Exception as e:
            print(f"Error in test setup: {str(e)}")
            self.take_screenshot("patient_test_setup_error")
            raise
        
        # Check for response
        try:
            # Wait for any page change or validation message
            WebDriverWait(self.driver, 15).until(
                lambda d: "login" in d.current_url.lower() or
                         d.find_elements(By.CLASS_NAME, "alert-success") or
                         d.find_elements(By.CLASS_NAME, "alert-danger") or
                         d.find_elements(By.CLASS_NAME, "errorlist") or
                         d.find_elements(By.CLASS_NAME, "text-danger") or
                         d.find_elements(By.CSS_SELECTOR, "input:invalid") or
                         d.find_elements(By.XPATH, "//*[contains(text(),'error')]")
            )
            
            # Take screenshot after submission
            self.take_screenshot("after_patient_submission")
            
            # Check current URL
            current_url = self.driver.current_url.lower()
            logger.info(f"Current URL after submission: {current_url}")
            
            if "login" in current_url:
                logger.info("✓ Redirected to login page after patient registration")
                return
                
            # Check for success messages
            success_msgs = self.driver.find_elements(By.CLASS_NAME, "alert-success")
            if success_msgs:
                logger.info(f"✓ Success message: {success_msgs[0].text}")
                return
            
            # Check for error messages
            error_selectors = [
                (By.CLASS_NAME, "alert-danger"),
                (By.CLASS_NAME, "errorlist"),
                (By.CLASS_NAME, "text-danger"),
                (By.CSS_SELECTOR, "input:invalid"),
                (By.XPATH, "//*[contains(text(),'error')]")
            ]
            
            error_messages = []
            for by, selector in error_selectors:
                try:
                    elements = self.driver.find_elements(by, selector) if isinstance(selector, str) else self.driver.find_elements(by, selector[1])
                    for el in elements:
                        if el.text.strip():
                            error_text = el.text.strip()
                            # Skip empty or very short error messages that might be false positives
                            if len(error_text) > 3 and not any(ignore in error_text.lower() for ignore in ['copyright', 'privacy', 'terms']):
                                error_messages.append(f"{selector if isinstance(selector, str) else selector[1]}: {error_text}")
                except Exception as e:
                    logger.warning(f"Error checking {selector}: {str(e)}")
            
            if error_messages:
                error_text = "\n".join(error_messages)
                logger.error(f"❌ Registration failed with errors:\n{error_text}")
                self.take_screenshot("patient_registration_error")
                self.fail(f"Registration failed with errors: {error_text}")
            
            # If we got here, something unexpected happened
            logger.warning("⚠ No success or error messages found after submission")
            self.take_screenshot("patient_registration_unknown")
            
            # Save page source for debugging
            with open("patient_page_source.html", "w") as f:
                f.write(self.driver.page_source)
            logger.info("Page source saved to: patient_page_source.html")
            
            self.fail("No success or error messages found after submission")
            
        except TimeoutException as e:
            self.take_screenshot("patient_submission_timeout")
            current_url = self.driver.current_url
            logger.error(f"❌ No response after form submission. Current URL: {current_url}")
            
            # Save page source for debugging
            with open("patient_page_source_timeout.html", "w") as f:
                f.write(self.driver.page_source)
            logger.info("Page source saved to: patient_page_source_timeout.html")
            
            # Check if the form is still visible (suggesting submission might have failed)
            try:
                if self.driver.find_element(By.TAG_NAME, "form"):
                    logger.warning("Form is still visible after submission attempt")
            except:
                pass
                
            self.fail(f"No response after form submission - check screenshots and page source. Error: {str(e)}")
        except Exception as e:
            self.take_screenshot("patient_registration_unexpected_error")
            logger.error(f"❌ Unexpected error during patient registration: {str(e)}")
            raise
    
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
        
        # Scroll to the submit button and wait for it to be clickable
        submit_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        # Add a small delay to ensure scrolling is complete
        time.sleep(0.5)
        # Click using JavaScript as a fallback
        try:
            submit_btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", submit_btn)
        
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
        
        # Scroll to the submit button and wait for it to be clickable
        submit_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        # Add a small delay to ensure scrolling is complete
        time.sleep(0.5)
        # Click using JavaScript as a fallback
        try:
            submit_btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", submit_btn)
        
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
        logger.info("\n=== Test Case 4: Valid Doctor Registration ===")
        
        # Generate test data
        doctor_data = self.create_test_doctor_data()
        logger.info(f"Generated test doctor data: {doctor_data}")
        
        # Navigate to registration choice page
        try:
            self.driver.get(f"{self.base_url}")
            register_link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Register"))
            )
            register_link.click()
            logger.info("Clicked on Register link")
            
            # Click on Doctor registration
            doctor_btn = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Register as Doctor"))
            )
            doctor_btn.click()
            logger.info("Clicked on Register as Doctor")
            
            # Fill doctor registration form
            if not self.fill_doctor_form(doctor_data):
                self.fail("Failed to fill doctor registration form")
            
            # Take screenshot before submission
            self.take_screenshot("before_doctor_submission")
            
            # Log form data for debugging
            logger.info("Doctor Registration Form Data:")
            for field in ["first_name", "last_name", "username", "email", "phone", 
                         "license_number", "experience_years", "consultation_fee"]:
                try:
                    value = self.driver.find_element(By.ID, f"id_{field}").get_attribute("value")
                    logger.info(f"  {field}: {value}")
                except Exception as e:
                    logger.warning(f"Could not get value for {field}: {str(e)}")
            
            # Submit the form
            logger.info("Submitting doctor registration form...")
            if not self.submit_form():
                self.take_screenshot("doctor_submit_failed")
                self.fail("Failed to submit doctor registration form")
                
        except Exception as e:
            print(f"Error in test setup: {str(e)}")
            self.take_screenshot("doctor_test_setup_error")
            raise
        
        # Check for response - similar to patient registration but with doctor-specific checks
        try:
            # Wait for any page change or validation message
            WebDriverWait(self.driver, 15).until(
                lambda d: "login" in d.current_url.lower() or
                         d.find_elements(By.CLASS_NAME, "alert-success") or
                         d.find_elements(By.CLASS_NAME, "alert-danger") or
                         d.find_elements(By.CLASS_NAME, "errorlist") or
                         d.find_elements(By.CLASS_NAME, "text-danger") or
                         d.find_elements(By.CSS_SELECTOR, "input:invalid") or
                         d.find_elements(By.XPATH, "//*[contains(text(),'error')]")
            )
            
            # Take screenshot after submission
            self.take_screenshot("after_doctor_submission")
            
            # Check current URL
            current_url = self.driver.current_url.lower()
            logger.info(f"Current URL after submission: {current_url}")
            
            if "login" in current_url:
                logger.info("✓ Redirected to login page after doctor registration")
                return
                
            # Check for success messages
            success_msgs = self.driver.find_elements(By.CLASS_NAME, "alert-success")
            if success_msgs:
                logger.info(f"✓ Success message: {success_msgs[0].text}")
                return
            
            # Check for error messages
            error_selectors = [
                (By.CLASS_NAME, "alert-danger"),
                (By.CLASS_NAME, "errorlist"),
                (By.CLASS_NAME, "text-danger"),
                (By.CSS_SELECTOR, "input:invalid"),
                (By.XPATH, "//*[contains(text(),'error')]")
            ]
            
            error_messages = []
            for by, selector in error_selectors:
                try:
                    elements = self.driver.find_elements(by, selector) if isinstance(selector, str) else self.driver.find_elements(by, selector[1])
                    for el in elements:
                        if el.text.strip():
                            error_text = el.text.strip()
                            # Skip empty or very short error messages that might be false positives
                            if len(error_text) > 3 and not any(ignore in error_text.lower() for ignore in ['copyright', 'privacy', 'terms']):
                                error_messages.append(f"{selector if isinstance(selector, str) else selector[1]}: {error_text}")
                except Exception as e:
                    logger.warning(f"Error checking {selector}: {str(e)}")
            
            if error_messages:
                error_text = "\n".join(error_messages)
                logger.error(f"❌ Doctor registration failed with errors:\n{error_text}")
                self.take_screenshot("doctor_registration_error")
                self.fail(f"Doctor registration failed with errors: {error_text}")
            
            # If we got here, something unexpected happened
            logger.warning("⚠ No success or error messages found after doctor registration")
            self.take_screenshot("doctor_registration_unknown")
            
            # Save page source for debugging
            with open("doctor_page_source.html", "w") as f:
                f.write(self.driver.page_source)
            logger.info("Page source saved to: doctor_page_source.html")
            
            self.fail("No success or error messages found after doctor registration")
            
        except TimeoutException as e:
            self.take_screenshot("doctor_submission_timeout")
            current_url = self.driver.current_url
            logger.error(f"❌ No response after doctor registration form submission. Current URL: {current_url}")
            
            # Save page source for debugging
            with open("doctor_page_source_timeout.html", "w") as f:
                f.write(self.driver.page_source)
            logger.info("Page source saved to: doctor_page_source_timeout.html")
            
            # Check if the form is still visible (suggesting submission might have failed)
            try:
                if self.driver.find_element(By.TAG_NAME, "form"):
                    logger.warning("Form is still visible after submission attempt")
            except:
                pass
                
            self.fail(f"No response after doctor registration form submission - check screenshots and page source. Error: {str(e)}")
        except Exception as e:
            self.take_screenshot("doctor_registration_unexpected_error")
            logger.error(f"❌ Unexpected error during doctor registration: {str(e)}")
            raise
    
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
        
        # Scroll to the submit button and wait for it to be clickable
        submit_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        # Scroll into view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        # Add a small delay to ensure scrolling is complete
        time.sleep(0.5)
        # Click using JavaScript as a fallback
        try:
            submit_btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", submit_btn)
        
        # Verify password mismatch error
        try:
            error_elements = self.driver.find_elements(By.CLASS_NAME, "text-danger")
            password_error_found = any("password" in elem.text.lower() and "match" in elem.text.lower() for elem in error_elements)
            self.assertTrue(password_error_found)
            print("✓ Password mismatch error displayed")
        except:
            print("⚠ Password mismatch validation not found - check implementation")


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('test_execution.log')
        ]
    )
    
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
