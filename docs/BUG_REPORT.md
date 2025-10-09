# MediBook - Bug Report Document

## Bug Report Summary

**Application:** MediBook - Doctor Appointment System  
**Version:** 1.0  
**Test Environment:** Django 4.2.7 + SQLite3  
**Testing Period:** October 9, 2025  
**Reported By:** STQA Testing Team  

---

## Bug Classification System

### Severity Levels
- **Critical (S1):** System crashes, data loss, security vulnerabilities
- **High (S2):** Major functionality broken, blocking workflows
- **Medium (S3):** Minor functionality issues, workarounds available
- **Low (S4):** Cosmetic issues, enhancement requests

### Priority Levels
- **P1:** Fix immediately
- **P2:** Fix in current release
- **P3:** Fix in next release
- **P4:** Fix when time permits

---

## Identified Bugs

### BUG-001: Missing Dashboard Templates
**Severity:** High (S2) | **Priority:** P1  
**Status:** Open  
**Reporter:** Test Team  
**Date:** 2025-10-09  

**Description:**  
Patient and doctor dashboard templates are not implemented, causing 500 errors when users try to access their dashboards after login.

**Steps to Reproduce:**
1. Login as patient (patient1/patient123)
2. Navigate to dashboard
3. Observe TemplateDoesNotExist error

**Expected Result:**  
Dashboard should display with user's appointments and relevant information.

**Actual Result:**  
TemplateDoesNotExist error for 'appointments/patient_dashboard.html'

**Environment:**  
- Browser: Chrome 118+
- OS: macOS
- Django: 4.2.7

**Screenshots:**  
Error page showing template not found

**Workaround:**  
None available

**Fix Recommendation:**  
Create missing template files:
- `templates/appointments/patient_dashboard.html`
- `templates/appointments/doctor_dashboard.html`

---

### BUG-002: Doctor Registration Form Missing Template
**Severity:** High (S2) | **Priority:** P1  
**Status:** Open  
**Reporter:** Test Team  
**Date:** 2025-10-09  

**Description:**  
Doctor registration form template is missing, preventing doctors from registering on the platform.

**Steps to Reproduce:**
1. Navigate to registration page
2. Click "Register as Doctor"
3. Observe TemplateDoesNotExist error

**Expected Result:**  
Doctor registration form should be displayed with all required fields.

**Actual Result:**  
TemplateDoesNotExist error for 'accounts/register_doctor.html'

**Fix Recommendation:**  
Create `templates/accounts/register_doctor.html` template

---

### BUG-003: Appointment Booking Form Missing Template
**Severity:** High (S2) | **Priority:** P1  
**Status:** Open  
**Reporter:** Test Team  
**Date:** 2025-10-09  

**Description:**  
Appointment booking form template is missing, preventing patients from booking appointments.

**Steps to Reproduce:**
1. Login as patient
2. Navigate to doctor list
3. Click "Book Appointment"
4. Observe TemplateDoesNotExist error

**Expected Result:**  
Appointment booking form should be displayed with date/time selection.

**Actual Result:**  
TemplateDoesNotExist error for 'appointments/book_appointment.html'

**Fix Recommendation:**  
Create `templates/appointments/book_appointment.html` template

---

### BUG-004: Profile Page Template Missing
**Severity:** Medium (S3) | **Priority:** P2  
**Status:** Open  
**Reporter:** Test Team  
**Date:** 2025-10-09  

**Description:**  
User profile page template is missing, preventing users from viewing/editing their profiles.

**Steps to Reproduce:**
1. Login as any user
2. Navigate to profile page
3. Observe TemplateDoesNotExist error

**Expected Result:**  
Profile page should display user information with edit options.

**Actual Result:**  
TemplateDoesNotExist error for 'accounts/profile.html'

**Fix Recommendation:**  
Create `templates/accounts/profile.html` template

---

### BUG-005: Static Files Not Loading in Production
**Severity:** Medium (S3) | **Priority:** P2  
**Status:** Open  
**Reporter:** Test Team  
**Date:** 2025-10-09  

**Description:**  
CSS and JavaScript files may not load properly in production environment due to static file configuration.

**Steps to Reproduce:**
1. Deploy application to production
2. Navigate to any page
3. Observe missing styles and JavaScript functionality

**Expected Result:**  
All static files should load correctly with proper styling.

**Actual Result:**  
Pages display without CSS styling and JavaScript functionality.

**Fix Recommendation:**  
- Configure static file serving for production
- Run `python manage.py collectstatic`
- Update web server configuration

---

### BUG-006: Email Validation Inconsistency
**Severity:** Low (S4) | **Priority:** P3  
**Status:** Open  
**Reporter:** Test Team  
**Date:** 2025-10-09  

**Description:**  
Email validation relies on HTML5 validation which may not be consistent across all browsers.

**Steps to Reproduce:**
1. Navigate to registration form
2. Enter invalid email format
3. Try to submit form
4. Behavior varies by browser

**Expected Result:**  
Consistent server-side email validation with clear error messages.

**Actual Result:**  
Validation behavior depends on browser HTML5 support.

**Fix Recommendation:**  
Implement server-side email validation with custom error messages.

---

### BUG-007: Phone Number Validation Edge Cases
**Severity:** Low (S4) | **Priority:** P3  
**Status:** Open  
**Reporter:** Test Team  
**Date:** 2025-10-09  

**Description:**  
Phone number validation accepts numbers with leading zeros but may not handle international formats.

**Steps to Reproduce:**
1. Enter phone number with international prefix (+91)
2. Try to submit registration form
3. Observe validation error

**Expected Result:**  
Support for international phone number formats.

**Actual Result:**  
Only accepts 10-digit numbers without country codes.

**Fix Recommendation:**  
Enhance phone validation to support international formats or clearly specify format requirements.

---

### BUG-008: Appointment Time Slot Conflicts
**Severity:** Medium (S3) | **Priority:** P2  
**Status:** Open  
**Reporter:** Test Team  
**Date:** 2025-10-09  

**Description:**  
System may allow double booking of the same time slot if multiple users submit simultaneously.

**Steps to Reproduce:**
1. Open two browser sessions
2. Login as different patients
3. Try to book same doctor at same time simultaneously
4. Both bookings may succeed

**Expected Result:**  
Only one booking should succeed, second should show error.

**Actual Result:**  
Race condition may allow double booking.

**Fix Recommendation:**  
Implement database-level constraints and proper transaction handling.

---

## Bug Statistics

### By Severity
- **Critical (S1):** 0 bugs
- **High (S2):** 3 bugs (37.5%)
- **Medium (S3):** 3 bugs (37.5%)
- **Low (S4):** 2 bugs (25.0%)

### By Priority
- **P1:** 3 bugs (37.5%)
- **P2:** 3 bugs (37.5%)
- **P3:** 2 bugs (25.0%)
- **P4:** 0 bugs

### By Status
- **Open:** 8 bugs (100%)
- **In Progress:** 0 bugs
- **Fixed:** 0 bugs
- **Closed:** 0 bugs

---

## Testing Recommendations

### Immediate Actions (P1)
1. Create all missing template files
2. Test complete user workflows
3. Verify all navigation links work

### Short-term Actions (P2)
1. Implement proper static file handling
2. Add database constraints for appointment conflicts
3. Enhance error handling and user feedback

### Long-term Actions (P3)
1. Improve form validation consistency
2. Add comprehensive input sanitization
3. Implement automated testing for edge cases

---

## Test Coverage Analysis

### Covered Areas ✅
- User registration flow
- Login/logout functionality
- Basic navigation
- Form field validation
- Database operations

### Areas Needing Coverage ❌
- Dashboard functionality
- Appointment management
- Profile management
- Error handling
- Security testing
- Performance testing

---

## Exploratory Testing Notes

### Positive Findings
- Database schema is well-designed
- User authentication works correctly
- Form validation prevents basic errors
- Responsive design framework in place

### Areas for Improvement
- Missing critical templates
- Incomplete user workflows
- Limited error handling
- Need for better user feedback

---

**Report Generated:** October 9, 2025  
**Next Review:** After template fixes are implemented  
**Contact:** STQA Testing Team
