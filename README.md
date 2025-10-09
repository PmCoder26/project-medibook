# MediBook - Doctor Appointment System

A comprehensive web-based application for managing doctor appointments with integrated testing framework for Software Testing and Quality Assurance (STQA).

## 🏥 Project Overview

**MediBook** is a Django-based web application that allows patients to book appointments with doctors online. The system includes user authentication, appointment management, and comprehensive testing coverage using Selenium WebDriver and IDE.

### 🎯 Key Features

- **User Management**: Separate registration for patients and doctors
- **Appointment Booking**: Real-time appointment scheduling system
- **Dashboard**: Role-based dashboards for patients and doctors
- **Doctor Search**: Filter doctors by specialization
- **Responsive Design**: Mobile-friendly Bootstrap interface
- **Comprehensive Testing**: Automated testing with Selenium

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite3 (Development)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Testing**: Selenium WebDriver, Selenium IDE
- **Authentication**: Django's built-in authentication system

## 📋 System Requirements

- Python 3.8+
- Django 4.2.7
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd stqa_project
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Sample Data
```bash
python populate_data.py
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The application will be available at: http://127.0.0.1:8000

## 👥 Test Credentials

### Sample Users
- **Admin**: `admin` / `admin123`
- **Doctors**: 
  - `dr_smith` / `doctor123` (Cardiology)
  - `dr_patel` / `doctor123` (Dermatology)
  - `dr_kumar` / `doctor123` (Orthopedics)
  - `dr_sharma` / `doctor123` (Pediatrics)
- **Patients**: 
  - `patient1` / `patient123` (Alice Johnson)
  - `patient2` / `patient123` (Bob Wilson)

## 🧪 Testing Framework

### Automated Testing
The project includes comprehensive automated testing using Selenium WebDriver:

#### Run All Tests
```bash
python run_tests.py
```

#### Individual Test Suites
```bash
# User Registration Tests
python tests/selenium_tests/test_user_registration.py

# Login System Tests
python tests/selenium_tests/test_login_system.py

# Appointment Booking Tests
python tests/selenium_tests/test_appointment_booking.py

# Regression Tests
python tests/regression_tests.py
```

### Test Coverage
- ✅ User Registration & Authentication
- ✅ Login/Logout System
- ✅ Doctor Listing & Search
- ✅ Appointment Booking Flow
- ✅ Form Validation
- ✅ Security Features
- ✅ Regression Testing

### Selenium IDE Tests
Import the test suite file: `tests/selenium_ide/medibook_test_suite.side`

## 📊 Test Reports

Test reports are automatically generated in `tests/test_reports/`:
- **HTML Report**: Comprehensive test execution report
- **Summary Report**: Text-based summary
- **Regression Report**: Detailed regression test results

## 🏗️ Project Structure

```
stqa_project/
├── medibook/                 # Django project settings
├── accounts/                 # User authentication app
├── appointments/             # Appointment management app
├── templates/                # HTML templates
├── static/                   # CSS, JS, images
├── tests/                    # Test files
│   ├── selenium_tests/       # WebDriver tests
│   ├── selenium_ide/         # IDE test suites
│   └── test_reports/         # Generated reports
├── docs/                     # Documentation
│   ├── TEST_PLAN.md         # Comprehensive test plan
│   └── BUG_REPORT.md        # Bug documentation
├── requirements.txt          # Python dependencies
├── manage.py                # Django management script
├── populate_data.py         # Sample data generator
└── run_tests.py            # Test execution script
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file (optional):
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_NAME=medibook_db
```

### Database Configuration
The project uses SQLite3 by default. To use PostgreSQL:

1. Install psycopg2: `pip install psycopg2-binary`
2. Update `settings.py` database configuration
3. Create PostgreSQL database
4. Run migrations

## 🎨 Features Overview

### For Patients
- Register and create profile
- Search doctors by specialization
- Book appointments with available time slots
- View appointment history
- Cancel appointments
- Dashboard with upcoming appointments

### For Doctors
- Professional registration with credentials
- Manage appointment schedule
- View patient appointments
- Update consultation fees
- Professional dashboard

### For Administrators
- User management via Django admin
- System monitoring
- Data management

## 🐛 Bug Tracking

Comprehensive bug tracking and classification system:
- **Severity Levels**: Critical, High, Medium, Low
- **Bug Categories**: Functional, UI/UX, Performance, Security
- **Detailed Reports**: See `docs/BUG_REPORT.md`

## 📈 Testing Methodology

### Test Plan Components
1. **Functional Testing**: Core feature validation
2. **Regression Testing**: Ensure existing functionality
3. **Security Testing**: Authentication and authorization
4. **UI/UX Testing**: User interface validation
5. **Performance Testing**: Load and response time testing

### Bug Taxonomy
- **Critical**: System crashes, data loss, security issues
- **High**: Major functionality broken
- **Medium**: Minor issues with workarounds
- **Low**: Cosmetic issues, enhancements

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure email settings
- [ ] Set up SSL/HTTPS
- [ ] Run security checks

### Static Files
```bash
python manage.py collectstatic
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is created for educational purposes as part of STQA coursework.

## 📞 Support

For issues and questions:
- Check the documentation in `docs/`
- Review test reports for known issues
- Create an issue in the repository

## 🎓 Educational Purpose

This project demonstrates:
- **Web Development**: Full-stack Django application
- **Testing Practices**: Comprehensive test coverage
- **Quality Assurance**: Bug tracking and reporting
- **Documentation**: Detailed project documentation
- **Best Practices**: Code organization and structure

---

**Project Created**: October 2025  
**Framework**: Django 4.2.7  
**Testing**: Selenium WebDriver & IDE  
**Purpose**: STQA Academic Project
