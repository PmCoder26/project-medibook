# MediBook - Test Plan Document

## 1. Introduction

### 1.1 Project Overview
**Application Name:** MediBook - Doctor Appointment System  
**Technology Stack:** Django + SQLite3 + Bootstrap + JavaScript  
**Purpose:** Online platform for booking and managing doctor appointments  

### 1.2 Test Objectives
- Validate all functional requirements
- Ensure data integrity and security
- Verify user interface responsiveness
- Test cross-browser compatibility
- Identify and document bugs with severity classification

## 2. Features to be Tested

### 2.1 User Authentication & Registration
#### 2.1.1 Patient Registration
- **Test Cases:**
  - Valid patient registration with all required fields
  - Registration with invalid email format
  - Registration with existing username/email
  - Password validation (minimum 8 characters, special characters)
  - Phone number validation (10 digits only)
  - Name validation (letters and spaces only)
  - Form field validation messages

#### 2.1.2 Doctor Registration
- **Test Cases:**
  - Valid doctor registration with medical license
  - Duplicate license number validation
  - Specialization selection
  - Experience years validation (0-50)
  - Consultation fee validation (positive decimal)

#### 2.1.3 Login System
- **Test Cases:**
  - Valid login with correct credentials
  - Invalid username/password combinations
  - Login with non-existent user
  - Session management after login
  - Redirect to appropriate dashboard based on user type

### 2.2 Doctor Management
#### 2.2.1 Doctor Listing
- **Test Cases:**
  - Display all available doctors
  - Filter doctors by specialization
  - Doctor profile information display
  - Availability status indication
  - Consultation fee display

#### 2.2.2 Doctor Search & Filter
- **Test Cases:**
  - Search functionality
  - Specialization filter dropdown
  - Clear filter functionality
  - No results handling

### 2.3 Appointment Booking System
#### 2.3.1 Appointment Creation
- **Test Cases:**
  - Book appointment with available doctor
  - Select valid date (future dates only)
  - Select available time slots
  - Prevent double booking of same slot
  - Appointment confirmation
  - Symptoms field (optional)

#### 2.3.2 Appointment Management
- **Test Cases:**
  - View upcoming appointments
  - View past appointments
  - Cancel appointments (before appointment time)
  - Appointment status updates
  - Appointment history tracking

### 2.4 Dashboard Functionality
#### 2.4.1 Patient Dashboard
- **Test Cases:**
  - Display upcoming appointments
  - Display past appointments
  - Quick access to book new appointment
  - Profile information display

#### 2.4.2 Doctor Dashboard
- **Test Cases:**
  - Display today's appointments
  - Display upcoming appointments
  - Appointment management options
  - Patient information access

### 2.5 Data Validation & Security
#### 2.5.1 Input Validation
- **Test Cases:**
  - SQL injection prevention
  - XSS attack prevention
  - CSRF token validation
  - Form field sanitization
  - File upload security (if applicable)

#### 2.5.2 Session Management
- **Test Cases:**
  - Session timeout handling
  - Logout functionality
  - Unauthorized access prevention
  - Role-based access control

## 3. Bug Taxonomy

### 3.1 Severity Classification

#### 3.1.1 Critical (Severity 1)
- **Definition:** System crashes, data loss, security vulnerabilities
- **Examples:**
  - Application crashes during user registration
  - Unauthorized access to patient data
  - Database corruption
  - Payment processing failures (if implemented)

#### 3.1.2 High (Severity 2)
- **Definition:** Major functionality broken, blocking user workflows
- **Examples:**
  - Unable to book appointments
  - Login system not working
  - Doctor search returning no results
  - Email notifications not sent

#### 3.1.3 Medium (Severity 3)
- **Definition:** Minor functionality issues, workarounds available
- **Examples:**
  - Incorrect validation messages
  - UI elements misaligned
  - Slow page loading
  - Minor calculation errors

#### 3.1.4 Low (Severity 4)
- **Definition:** Cosmetic issues, enhancement requests
- **Examples:**
  - Spelling mistakes
  - Color scheme issues
  - Font size inconsistencies
  - Missing tooltips

### 3.2 Bug Categories

#### 3.2.1 Functional Bugs
- Login/logout issues
- Form validation failures
- Incorrect calculations
- Workflow interruptions

#### 3.2.2 UI/UX Bugs
- Layout issues
- Responsive design problems
- Navigation difficulties
- Accessibility issues

#### 3.2.3 Performance Bugs
- Slow page load times
- Database query optimization
- Memory leaks
- Timeout issues

#### 3.2.4 Security Bugs
- Authentication bypasses
- Data exposure
- Input validation failures
- Session management issues

#### 3.2.5 Compatibility Bugs
- Browser-specific issues
- Mobile device problems
- Operating system conflicts
- Version compatibility

## 4. Test Environment

### 4.1 System Requirements
- **Operating System:** macOS, Windows, Linux
- **Browsers:** Chrome, Firefox, Safari, Edge
- **Python Version:** 3.8+
- **Django Version:** 4.2.7
- **Database:** SQLite3

### 4.2 Test Data
- **Sample Doctors:** 4 doctors with different specializations
- **Sample Patients:** 2 test patients
- **Time Slots:** 16 available time slots (9 AM - 6 PM)
- **Admin User:** For administrative testing

## 5. Test Execution Strategy

### 5.1 Manual Testing
- Exploratory testing for user experience
- Boundary value testing for form inputs
- Negative testing for error handling
- Cross-browser compatibility testing

### 5.2 Automated Testing
- **Selenium WebDriver:** For functional test automation
- **Selenium IDE:** For record and playback testing
- **Unit Tests:** For individual component testing
- **Integration Tests:** For workflow testing

### 5.3 Regression Testing
- Automated test suite execution
- Critical path testing
- Smoke testing for new builds
- Performance regression testing

## 6. Test Deliverables

### 6.1 Test Documentation
- Test Plan (this document)
- Test Cases and Test Scripts
- Bug Reports with screenshots
- Test Execution Reports
- Regression Test Results

### 6.2 Automated Test Assets
- Selenium WebDriver test scripts
- Selenium IDE test suites (.side files)
- Test data files
- Configuration files

## 7. Entry and Exit Criteria

### 7.1 Entry Criteria
- Application deployed and accessible
- Test environment setup complete
- Test data prepared
- Testing tools configured

### 7.2 Exit Criteria
- All planned test cases executed
- Critical and high severity bugs resolved
- Test coverage > 90%
- Performance benchmarks met
- Documentation complete

## 8. Risk Assessment

### 8.1 High Risk Areas
- User authentication and authorization
- Appointment booking logic
- Data validation and sanitization
- Session management

### 8.2 Mitigation Strategies
- Comprehensive test coverage for critical features
- Security-focused testing
- Performance testing under load
- Regular regression testing

---

**Document Version:** 1.0  
**Last Updated:** October 9, 2025  
**Prepared By:** STQA Testing Team
