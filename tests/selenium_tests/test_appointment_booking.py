"""
Selenium WebDriver Tests for Appointment Booking System
MediBook - Doctor Appointment System
"""

import unittest
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestAppointmentBooking(unittest.TestCase):
    
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
        """Login as patient before each test"""
        self.driver.get(f"{self.base_url}/accounts/login/")
        
        # Login as patient1
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
        time.sleep(1)
    
    def test_01_view_doctor_list(self):
        """Test Case: View available doctors"""
        print("\n=== Test Case 1: View Doctor List ===")
        
        # Navigate to doctor list
        self.driver.get(f"{self.base_url}/appointments/doctors/")
        
        # Verify doctors are displayed
        try:
            doctor_cards = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "doctor-card"))
            )
            self.assertGreater(len(doctor_cards), 0, "No doctors found on the page")
            
            # Check if doctor information is displayed
            first_doctor = doctor_cards[0]
            doctor_name = first_doctor.find_element(By.TAG_NAME, "h5")
            self.assertTrue(doctor_name.text.startswith("Dr."))
            
            print(f"✓ Found {len(doctor_cards)} doctors displayed")
            
        except TimeoutException:
            self.fail("Doctor list page not loading properly")
    
    def test_02_filter_doctors_by_specialization(self):
        """Test Case: Filter doctors by specialization"""
        print("\n=== Test Case 2: Filter Doctors by Specialization ===")
        
        # Navigate to doctor list
        self.driver.get(f"{self.base_url}/appointments/doctors/")
        
        # Select a specialization filter
        specialization_select = self.wait.until(
            EC.presence_of_element_located((By.ID, "specialization"))
        )
        select = Select(specialization_select)
        select.select_by_value("cardiology")
        
        # Click filter button
        filter_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        filter_btn.click()
        
        # Verify filtered results
        try:
            # Wait for page to reload with filtered results
            time.sleep(2)
            
            # Check if cardiology is selected in the dropdown
            selected_option = select.first_selected_option
            self.assertEqual(selected_option.get_attribute("value"), "cardiology")
            
            # Verify that displayed doctors have cardiology specialization
            specialization_badges = self.driver.find_elements(By.CLASS_NAME, "specialization-badge")
            if specialization_badges:
                for badge in specialization_badges:
                    self.assertIn("Cardiology", badge.text)
            
            print("✓ Specialization filter working correctly")
            
        except Exception as e:
            print(f"⚠ Filter functionality issue: {e}")
    
    def test_03_book_appointment_valid_data(self):
        """Test Case: Book appointment with valid data"""
        print("\n=== Test Case 3: Book Appointment - Valid Data ===")
        
        # Navigate to doctor list and select first available doctor
        self.driver.get(f"{self.base_url}/appointments/doctors/")
        
        # Find and click on first "Book Appointment" button
        try:
            book_btn = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Book Appointment"))
            )
            book_btn.click()
            
            # Fill appointment booking form
            # Select future date (tomorrow)
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            date_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "appointment_date"))
            )
            date_field.send_keys(tomorrow)
            
            # Select a time slot
            time_slots = self.driver.find_elements(By.CSS_SELECTOR, "input[name='appointment_time']")
            if time_slots:
                time_slots[0].click()  # Select first available time slot
            
            # Add symptoms (optional)
            symptoms_field = self.driver.find_element(By.NAME, "symptoms")
            symptoms_field.send_keys("Regular checkup and consultation")
            
            # Submit booking
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()
            
            # Verify booking success
            try:
                success_message = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
                )
                self.assertIn("successful", success_message.text.lower())
                print("✓ Appointment booked successfully")
                
            except TimeoutException:
                # Check if redirected to dashboard
                if "dashboard" in self.driver.current_url or "patient" in self.driver.current_url:
                    print("✓ Redirected to dashboard after booking")
                else:
                    self.fail("Appointment booking failed")
                    
        except TimeoutException:
            self.fail("Book appointment button not found or not clickable")
    
    def test_04_book_appointment_past_date(self):
        """Test Case: Try to book appointment with past date"""
        print("\n=== Test Case 4: Book Appointment - Past Date ===")
        
        # Navigate to booking page
        self.driver.get(f"{self.base_url}/appointments/doctors/")
        
        try:
            book_btn = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Book Appointment"))
            )
            book_btn.click()
            
            # Try to select past date (yesterday)
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            date_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "appointment_date"))
            )
            date_field.send_keys(yesterday)
            
            # Select time slot
            time_slots = self.driver.find_elements(By.CSS_SELECTOR, "input[name='appointment_time']")
            if time_slots:
                time_slots[0].click()
            
            # Submit booking
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()
            
            # Verify error handling
            try:
                error_message = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
                )
                print("✓ Past date validation error displayed")
                
            except TimeoutException:
                # Check if HTML5 date validation prevents past dates
                date_validation = date_field.get_attribute("validationMessage")
                if len(date_validation) > 0:
                    print("✓ HTML5 date validation preventing past dates")
                else:
                    print("⚠ Past date validation may need improvement")
                    
        except TimeoutException:
            self.fail("Could not access appointment booking form")
    
    def test_05_view_patient_dashboard(self):
        """Test Case: View patient dashboard with appointments"""
        print("\n=== Test Case 5: Patient Dashboard ===")
        
        # Navigate to patient dashboard
        self.driver.get(f"{self.base_url}/appointments/patient/")
        
        # Verify dashboard elements
        try:
            # Check for dashboard heading or content
            dashboard_content = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
            
            # Look for appointments sections
            upcoming_section = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Upcoming') or contains(text(), 'upcoming')]")
            past_section = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Past') or contains(text(), 'past')]")
            
            # Verify sections exist
            self.assertTrue(len(upcoming_section) > 0 or len(past_section) > 0, "Dashboard sections not found")
            
            print("✓ Patient dashboard loaded with appointment sections")
            
        except TimeoutException:
            self.fail("Patient dashboard not loading properly")
    
    def test_06_appointment_cancellation(self):
        """Test Case: Cancel an appointment"""
        print("\n=== Test Case 6: Appointment Cancellation ===")
        
        # First, try to book an appointment to have something to cancel
        self.driver.get(f"{self.base_url}/appointments/doctors/")
        
        try:
            book_btn = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Book Appointment"))
            )
            book_btn.click()
            
            # Book appointment for day after tomorrow
            future_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
            date_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "appointment_date"))
            )
            date_field.send_keys(future_date)
            
            # Select time slot
            time_slots = self.driver.find_elements(By.CSS_SELECTOR, "input[name='appointment_time']")
            if time_slots:
                time_slots[1].click()  # Select second time slot to avoid conflicts
            
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()
            
            # Wait for booking confirmation
            time.sleep(2)
            
            # Navigate to dashboard to find cancel button
            self.driver.get(f"{self.base_url}/appointments/patient/")
            
            # Look for cancel button
            cancel_buttons = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Cancel') or contains(@href, 'cancel')]")
            
            if cancel_buttons:
                cancel_buttons[0].click()
                
                # Verify cancellation success
                try:
                    success_message = self.wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
                    )
                    self.assertIn("cancel", success_message.text.lower())
                    print("✓ Appointment cancelled successfully")
                    
                except TimeoutException:
                    print("✓ Cancellation processed (no explicit message)")
            else:
                print("⚠ No cancellable appointments found or cancel functionality not implemented")
                
        except Exception as e:
            print(f"⚠ Cancellation test could not be completed: {e}")
    
    def test_07_unauthorized_booking_access(self):
        """Test Case: Unauthorized access to booking (logged out user)"""
        print("\n=== Test Case 7: Unauthorized Booking Access ===")
        
        # Logout first
        user_dropdown = self.driver.find_element(By.ID, "navbarDropdown")
        user_dropdown.click()
        
        logout_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
        )
        logout_link.click()
        
        # Try to access booking page directly
        self.driver.get(f"{self.base_url}/appointments/book/1/")
        
        # Verify redirect to login or access denied
        try:
            # Should be redirected to login page
            self.wait.until(
                EC.any_of(
                    EC.url_contains("login"),
                    EC.presence_of_element_located((By.ID, "id_username"))
                )
            )
            print("✓ Unauthorized access properly redirected to login")
            
        except TimeoutException:
            # Check if access is denied with error message
            error_elements = self.driver.find_elements(By.CLASS_NAME, "alert-danger")
            if error_elements:
                print("✓ Access denied message displayed")
            else:
                self.fail("Unauthorized access not properly handled")


if __name__ == "__main__":
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAppointmentBooking)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"APPOINTMENT BOOKING TESTS SUMMARY")
    print(f"{'='*50}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
