#!/usr/bin/env python3
"""
Simple Selenium Test for MediBook Application
Tests basic functionality without complex driver management
"""

import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class SimpleMediBookTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up the WebDriver before running tests"""
        try:
            # Try Safari first (usually available on Mac)
            cls.driver = webdriver.Safari()
            print("✅ Using Safari WebDriver")
        except Exception as e:
            print(f"Safari failed: {e}")
            try:
                # Try Chrome without driver manager
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                cls.driver = webdriver.Chrome(options=options)
                print("✅ Using Chrome WebDriver")
            except Exception as e2:
                print(f"Chrome failed: {e2}")
                raise unittest.SkipTest("No compatible browser found")
        
        cls.driver.maximize_window()
        cls.base_url = "http://127.0.0.1:8000"
        cls.wait = WebDriverWait(cls.driver, 10)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        if hasattr(cls, 'driver'):
            cls.driver.quit()
    
    def test_01_homepage_loads(self):
        """Test that the homepage loads successfully"""
        print("\n🧪 Testing homepage load...")
        try:
            self.driver.get(self.base_url)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Check if MediBook title is present
            self.assertIn("MediBook", self.driver.title)
            print("✅ Homepage loaded successfully")
            
        except Exception as e:
            print(f"❌ Homepage test failed: {e}")
            raise
    
    def test_02_navigation_links(self):
        """Test that navigation links are present"""
        print("\n🧪 Testing navigation links...")
        try:
            self.driver.get(self.base_url)
            
            # Check for navigation links
            home_link = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Home")))
            self.assertTrue(home_link.is_displayed())
            
            find_doctors_link = self.driver.find_element(By.LINK_TEXT, "Find Doctors")
            self.assertTrue(find_doctors_link.is_displayed())
            
            login_link = self.driver.find_element(By.LINK_TEXT, "Login")
            self.assertTrue(login_link.is_displayed())
            
            register_link = self.driver.find_element(By.LINK_TEXT, "Register")
            self.assertTrue(register_link.is_displayed())
            
            print("✅ All navigation links found")
            
        except Exception as e:
            print(f"❌ Navigation test failed: {e}")
            raise
    
    def test_03_login_page_access(self):
        """Test accessing the login page"""
        print("\n🧪 Testing login page access...")
        try:
            self.driver.get(f"{self.base_url}/accounts/login/")
            
            # Check for login form elements
            username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            password_field = self.driver.find_element(By.NAME, "password")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            
            self.assertTrue(username_field.is_displayed())
            self.assertTrue(password_field.is_displayed())
            self.assertTrue(login_button.is_displayed())
            
            print("✅ Login page accessible with all form elements")
            
        except Exception as e:
            print(f"❌ Login page test failed: {e}")
            raise
    
    def test_04_patient_login(self):
        """Test patient login functionality"""
        print("\n🧪 Testing patient login...")
        try:
            self.driver.get(f"{self.base_url}/accounts/login/")
            
            # Fill login form
            username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            password_field = self.driver.find_element(By.NAME, "password")
            
            username_field.clear()
            username_field.send_keys("patient1")
            password_field.clear()
            password_field.send_keys("patient123")
            
            # Submit form
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for redirect and check if we're on patient dashboard
            time.sleep(2)
            current_url = self.driver.current_url
            
            # Should redirect to patient dashboard
            self.assertTrue("/appointments/patient/" in current_url or "patient" in current_url.lower())
            print("✅ Patient login successful")
            
            # Logout
            try:
                logout_link = self.driver.find_element(By.LINK_TEXT, "Logout")
                logout_link.click()
                time.sleep(1)
            except:
                pass  # Logout link might not be visible
            
        except Exception as e:
            print(f"❌ Patient login test failed: {e}")
            raise
    
    def test_05_doctor_list_access(self):
        """Test accessing the doctor list"""
        print("\n🧪 Testing doctor list access...")
        try:
            self.driver.get(f"{self.base_url}/appointments/doctors/")
            
            # Check if page loads
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Look for doctor-related content
            page_source = self.driver.page_source.lower()
            self.assertTrue("doctor" in page_source or "dr." in page_source)
            
            print("✅ Doctor list page accessible")
            
        except Exception as e:
            print(f"❌ Doctor list test failed: {e}")
            raise

def run_tests():
    """Run all tests and provide summary"""
    print("🚀 Starting MediBook Selenium Tests...")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleMediBookTest)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate == 100:
            print("🎉 All tests passed! Selenium is working correctly.")
        elif success_rate >= 80:
            print("✅ Most tests passed. Minor issues detected.")
        else:
            print("⚠️ Several tests failed. Check the application setup.")
    else:
        print("❌ No tests ran successfully.")
    
    print("=" * 60)
    
    return result.testsRun > 0 and len(result.failures) == 0 and len(result.errors) == 0

if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
