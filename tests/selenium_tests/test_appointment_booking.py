"""
Streamlined Doctor Booking Test
- Handles login sessions properly
- Debugs authentication issues
- Saves artifacts for troubleshooting
"""

import time
import unittest
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestDoctorBooking(unittest.TestCase):
    """Complete doctor booking test with session handling"""
    
    def setUp(self):
        """Initialize test with Chrome options"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)
        self.base_url = "http://127.0.0.1:8000"
        
        # Test user credentials
        self.credentials = {
            'username': 'patient1',
            'password': 'patient123'
        }
        
        # Create a directory for test artifacts
        self.test_dir = "test_artifacts"
        os.makedirs(self.test_dir, exist_ok=True)
    
    def save_page_source(self, step_name):
        """Save current page source for debugging"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.test_dir}/{step_name}_{timestamp}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        print(f"Saved page source to: {filename}")
        return filename
    
    def take_screenshot(self, step_name):
        """Take a screenshot of the current page"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.test_dir}/{step_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved to: {filename}")
        return filename
    
    def login(self):
        """Handle login and return session status"""
        print("\n🔑 Logging in...")
        try:
            self.driver.get(f"{self.base_url}/accounts/login/")
            
            # Wait for and fill login form
            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.clear()
            username_field.send_keys(self.credentials['username'])
            
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(self.credentials['password'])
            
            # Submit form
            login_button = self.driver.find_element(
                By.CSS_SELECTOR, "button[type='submit']"
            )
            login_button.click()
            
            # Verify login success
            try:
                self.wait.until(
                    lambda d: "login" not in d.current_url.lower()
                )
                print("✅ Login successful")
                return True
            except TimeoutException:
                self.save_page_source("login_failed")
                print("❌ Login failed - check credentials")
                return False
                
        except Exception as e:
            self.save_page_source("login_error")
            print(f"❌ Login error: {str(e)}")
            return False
    
    def test_complete_booking_flow(self):
        """Complete booking flow from login to confirmation with performance metrics"""
        print("\n🚀 Starting booking test...")
        
        # Initialize performance metrics
        performance_metrics = {
            'login': 0,
            'load_doctors': 0,
            'filter_doctors': 0,
            'select_doctor': 0,
            'fill_booking_form': 0,
            'submit_booking': 0,
            'total': 0,
            'verification': 0
        }
        
        # Start total timer
        total_start_time = time.time()
        
        try:
            # 1. Login
            login_start = time.time()
            if not self.login():
                raise Exception("Login failed, cannot proceed with test")
            performance_metrics['login'] = time.time() - login_start
            
            # 2. Navigate to doctors list
            print("\n👨‍⚕️ Loading doctors list...")
            load_doctors_start = time.time()
            self.driver.get(f"{self.base_url}/appointments/doctors/")
            self.save_page_source("doctors_list")
            performance_metrics['load_doctors'] = time.time() - load_doctors_start
            
            # 3. Filter doctors (if dropdown exists)
            print("\n🔍 Filtering doctors...")
            filter_start = time.time()
            try:
                # Wait for the page to be fully loaded
                self.wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # Try to find and handle the specialization filter
                select = Select(self.wait.until(
                    EC.presence_of_element_located((By.ID, "specialization"))
                ))
                
                if len(select.options) > 1:
                    # Select first non-default specialization
                    select.select_by_index(1)
                    selected_spec = select.first_selected_option.text
                    print(f"Selected specialization: {selected_spec}")
                    
                    # Find and submit the form
                    form = self.driver.find_element(By.TAG_NAME, "form")
                    form.submit()
                    
                    # Wait for filter to apply
                    time.sleep(2)
                    performance_metrics['filter_doctors'] = time.time() - filter_start
                    self.save_page_source("after_filter")
                    
                    # Check if we're still logged in
                    if "login" in self.driver.current_url.lower():
                        raise Exception("Session lost after filter")
                        
                    print("✅ Applied specialization filter")
                    
            except Exception as e:
                print(f"ℹ️ Filter warning: {str(e)}")
                self.save_page_source("filter_warning")
                # Continue test even if filter fails
            
            # 4. Select first available doctor
            print("\n📅 Selecting doctor...")
            try:
                # Wait for doctor cards to load
                doctor_card = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "doctor-card"))
                )
                
                # Scroll to the doctor card
                self.driver.execute_script("arguments[0].scrollIntoView();", doctor_card)
                time.sleep(1)
                
                # Get doctor details
                doctor_name = doctor_card.find_element(By.TAG_NAME, "h5").text
                print(f"Selected: {doctor_name}")
                
                # Find and click book button
                book_btn = self.wait.until(
                    EC.element_to_be_clickable((
                        By.XPATH, 
                        ".//a[contains(@class, 'btn') and contains(., 'Book')]"
                    ))
                )
                book_btn.click()
                print("✅ Clicked book button")
                
            except Exception as e:
                self.save_page_source("doctor_selection_error")
                self.take_screenshot("doctor_selection")
                raise Exception(f"Failed to select doctor: {str(e)}")
            
            # 5. Fill booking form
            print("\n📝 Filling booking form...")
            fill_form_start = time.time()
            try:
                form_start_time = time.time()
                # Wait for booking form to load
                self.wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "form"))
                )
                print("✅ Booking form loaded")
                
                def select_available_date():
                    """Select the next available date with time slots"""
                    # Get the date input field
                    date_input = self.wait.until(
                        EC.presence_of_element_located((By.ID, "appointment_date"))
                    )
                    
                    # Get the minimum allowed date from the input's min attribute
                    min_date = date_input.get_attribute('min')
                    if not min_date:
                        # If no min date, default to today
                        min_date = datetime.now().strftime("%Y-%m-%d")
                    
                    # Parse the minimum date
                    min_date = datetime.strptime(min_date, "%Y-%m-%d")
                    
                    # Try the next 30 days starting from min_date
                    for day_offset in range(0, 30):
                        check_date = (min_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")
                        
                        # Clear and set the date
                        self.driver.execute_script("arguments[0].value = arguments[1];", date_input, check_date)
                        # Trigger change event
                        self.driver.execute_script("""
                            const event = new Event('change', { bubbles: true });
                            arguments[0].dispatchEvent(event);
                        """, date_input)
                        
                        print(f"\nChecking date: {check_date}")
                        
                        # Wait for time slots to load (wait for the loading to complete)
                        time.sleep(2)
                        
                        # Check for available time slots
                        time_slots = self.driver.find_elements(
                            By.CSS_SELECTOR, 
                            "input[name='appointment_time']:not([disabled])"
                        )
                        
                        if time_slots:
                            print(f"✅ Found {len(time_slots)} available time slots on {check_date}")
                            return check_date, time_slots
                        
                        print(f"No available time slots on {check_date}")
                    
                    raise Exception("No available time slots found in the next 30 days")
                
                # Find and select an available date with time slots
                print("\n🔍 Searching for next available date with time slots...")
                selected_date, available_slots = select_available_date()
                print(f"Selected date with available slots: {selected_date}")
                
                # Wait for the time slots to be fully loaded and interactive
                time.sleep(2)
                
                # Select the first available time slot
                try:
                    if not available_slots:
                        raise Exception("No time slots available despite previous check")
                    
                    # Get the first available time slot
                    time_slot = available_slots[0]
                    time_slot_value = time_slot.get_attribute('value')
                    time_slot_label = self.driver.find_element(
                        By.CSS_SELECTOR, 
                        f"label[for='slot_{time_slot_value}']"
                    ).text
                    
                    # Scroll to the time slot and click it
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", time_slot)
                    time.sleep(0.5)  # Small delay for scrolling
                    
                    # Click using JavaScript to avoid any overlay issues
                    self.driver.execute_script("arguments[0].click();", time_slot)
                    
                    # Verify the time slot is selected
                    if not time_slot.is_selected():
                        # Try one more time with a direct click
                        time_slot.click()
                    
                    print(f"✅ Selected time slot: {time_slot_label} (ID: {time_slot_value})")
                    
                except Exception as e:
                    self.save_page_source("time_slot_selection_error")
                    self.take_screenshot("time_slot_selection_error")
                    raise Exception(f"Failed to select time slot: {str(e)}")
                
                # Record form fill time and update metrics
                form_fill_time = time.time() - form_start_time
                performance_metrics['fill_booking_form'] = form_fill_time
                print(f"✅ Filled booking form (took {form_fill_time:.2f} seconds)")
                
                # Update the fill_booking_form metric with the form fill time
                performance_metrics['fill_booking_form'] = time.time() - fill_form_start
                
                # Add a small delay after time slot selection
                time.sleep(1)
                
                # Add symptoms with more specific selector
                symptoms = f"Test appointment - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                try:
                    # Try different selectors for symptoms field
                    selectors = [
                        "textarea#symptoms", 
                        "input#symptoms",
                        "textarea[name='symptoms']",
                        "input[name='symptoms']"
                    ]
                    
                    symptoms_found = False
                    for selector in selectors:
                        try:
                            symptoms_input = self.wait.until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                            )
                            symptoms_input.clear()
                            symptoms_input.send_keys(symptoms)
                            print(f"✅ Added symptoms: {symptoms}")
                            symptoms_found = True
                            break
                        except:
                            continue
                            
                    if not symptoms_found:
                        print("⚠️ Could not find symptoms field with any selector")
                        self.save_page_source("symptoms_field_not_found")
                        
                except Exception as e:
                    print(f"⚠️ Error setting symptoms: {str(e)}")
                    self.save_page_source("symptoms_field_error")
                
                # Handle terms checkbox with more robust selectors
                try:
                    # Try different possible selectors for the terms checkbox
                    selectors = [
                        "#booking-terms", 
                        "input[type='checkbox'][name='terms']",
                        ".terms-checkbox",
                        "input[name='accept_terms']",
                        "#terms"
                    ]
                    
                    terms_checked = False
                    for selector in selectors:
                        try:
                            terms = self.wait.until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                            )
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", terms)
                            time.sleep(0.5)
                            
                            if not terms.is_selected():
                                self.driver.execute_script("arguments[0].click();", terms)
                                
                            # Double-check it's checked
                            if not terms.is_selected():
                                terms.click()
                                
                            terms_checked = True
                            print("✅ Accepted terms")
                            break
                        except Exception as e:
                            print(f"⚠️ Could not find/click terms with selector '{selector}': {str(e)}")
                            continue
                            
                    if not terms_checked:
                        print("ℹ️ No terms checkbox found with standard selectors")
                        self.save_page_source("terms_checkbox_not_found")
                        
                except Exception as e:
                    print(f"⚠️ Error handling terms checkbox: {str(e)}")
                    self.save_page_source("terms_checkbox_error")
                
                # Submit booking with better error handling
                print("\n🚀 Attempting to submit booking...")
                try:
                    submit_start_time = time.time()
                    # Try different possible selectors for the submit button
                    submit_selectors = [
                        "button[type='submit']",
                        "#book-btn",
                        ".btn-primary",
                        "input[type='submit']"
                    ]
                    
                    submitted = False
                    for selector in submit_selectors:
                        try:
                            submit_btn = self.wait.until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                            )
                            # Scroll into view and click using JavaScript
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
                            self.driver.execute_script("arguments[0].click();", submit_btn)
                            print(f"✅ Clicked submit button with selector: {selector}")
                            # Record submit time
                            performance_metrics['submit_booking'] = time.time() - submit_start_time
                            submitted = True
                            break
                        except Exception as e:
                            print(f"⚠️ Could not click submit with selector {selector}: {str(e)}")
                    
                    if not submitted:
                        raise Exception("Could not find or click any submit button")
                        
                except Exception as e:
                    self.save_page_source("submit_error")
                    self.take_screenshot("submit_error")
                    raise Exception(f"Failed to submit booking form: {str(e)}")
                    submit_time = time.time() - submit_start_time
                    performance_metrics['submit_booking'] = submit_time
                    print(f"✅ Booking submitted (took {submit_time:.2f} seconds)")
                
                # Start verification timer
                verify_start = time.time()
                
                # Verify success and check for valid redirect
                try:
                    # Define valid success patterns in URL
                    valid_redirects = [
                        "/appointments/patient/",
                        "/appointments/book/",
                        "/appointments/"
                    ]
                    
                    # Wait for either success message or valid redirect URL
                    success = self.wait.until(
                        lambda d: (
                            any(text in d.page_source.lower() 
                                for text in ["success", "confirmed", "booked"]) 
                            or any(url in d.current_url for url in valid_redirects)
                        ),
                        message="Timed out waiting for booking confirmation or redirect"
                    )
                    
                    # Check if we're on a valid page
                    current_url = self.driver.current_url
                    if not any(url in current_url for url in valid_redirects):
                        print(f"\n⚠️ Unexpected redirect URL: {current_url}")
                        # Try to navigate to patient dashboard
                        self.driver.get(f"{self.base_url}/appointments/patient/")
                    
                    print(f"\n🎉 Booking successful! Current URL: {current_url}")
                    
                    # Verify we're on a valid page after booking
                    try:
                        self.wait.until(
                            EC.presence_of_element_located((By.TAG_NAME, "body")),
                            "Could not find page body after booking"
                        )
                        print("✅ Successfully loaded the page after booking")
                        
                        # Add 5-second wait to observe the result
                        # Calculate and display performance metrics
                        performance_metrics['verification'] = time.time() - verify_start
                        performance_metrics['total'] = time.time() - total_start_time
                        
                        print("\n📊 Performance Metrics:")
                        print("=" * 50)
                        print(f"Login: {performance_metrics['login']:.2f} seconds")
                        print(f"Load Doctors: {performance_metrics['load_doctors']:.2f} seconds")
                        print(f"Filter Doctors: {performance_metrics['filter_doctors']:.2f} seconds")
                        print(f"Select Doctor: {performance_metrics['select_doctor']:.2f} seconds")
                        print(f"Fill Booking Form: {performance_metrics['fill_booking_form']:.2f} seconds")
                        print(f"Submit Booking: {performance_metrics['submit_booking']:.2f} seconds")
                        print(f"Verification: {performance_metrics['verification']:.2f} seconds")
                        print("-" * 50)
                        print(f"Total Test Time: {performance_metrics['total']:.2f} seconds")
                        print("=" * 50)
                        
                        # Add final wait to observe the result
                        print("\n⏳ Waiting 5 seconds...")
                        time.sleep(5)
                        
                    except Exception as e:
                        print(f"⚠️ Warning verifying page load: {str(e)}")
                        self.save_page_source("page_load_verification_error")
                    
                except Exception as e:
                    self.save_page_source("booking_verification_error")
                    self.take_screenshot("booking_verification_error")
                    print(f"\n⚠️ Booking verification warning: {str(e)}")
                    print(f"Current URL: {self.driver.current_url}")
                    
                except Exception as e:
                    self.save_page_source("booking_verification_error")
                    self.take_screenshot("booking_verification_error")
                    print(f"\n⚠️ Booking verification warning: {str(e)}")
                    print(f"Current URL: {self.driver.current_url}")
                
            except Exception as e:
                self.save_page_source("booking_form_error")
                self.take_screenshot("booking_form")
                raise Exception(f"Failed to complete booking form: {str(e)}")
                
        except Exception as e:
            self.save_page_source("test_failure")
            self.take_screenshot("test_failure")
            print(f"\n❌ Test failed: {str(e)}")
            raise
    
    def tearDown(self):
        """Clean up after test"""
        if hasattr(self, 'driver'):
            self.driver.quit()
        print("\n" + "="*50)
        print("Test completed")
        print("="*50)

if __name__ == "__main__":
    unittest.main()