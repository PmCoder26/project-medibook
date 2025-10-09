#!/usr/bin/env python
import os
import sys
import django
from datetime import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medibook.settings')
django.setup()

from accounts.models import User, Doctor, Patient
from appointments.models import TimeSlot, DoctorAvailability

def create_sample_data():
    print("Creating sample data...")
    
    # Create time slots
    time_slots = [
        '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00',
        '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00'
    ]
    
    for slot in time_slots:
        TimeSlot.objects.get_or_create(time=slot)
    
    print(f"Created {len(time_slots)} time slots")
    
    # Create sample doctors
    doctors_data = [
        {
            'username': 'dr_smith',
            'email': 'dr.smith@medibook.com',
            'first_name': 'John',
            'last_name': 'Smith',
            'phone': '9876543210',
            'specialization': 'cardiology',
            'license_number': 'MED001',
            'experience_years': 15,
            'consultation_fee': 1500.00,
            'bio': 'Experienced cardiologist with expertise in heart diseases and cardiac surgery.'
        },
        {
            'username': 'dr_patel',
            'email': 'dr.patel@medibook.com',
            'first_name': 'Priya',
            'last_name': 'Patel',
            'phone': '9876543211',
            'specialization': 'dermatology',
            'license_number': 'MED002',
            'experience_years': 8,
            'consultation_fee': 1200.00,
            'bio': 'Dermatologist specializing in skin care and cosmetic treatments.'
        },
        {
            'username': 'dr_kumar',
            'email': 'dr.kumar@medibook.com',
            'first_name': 'Raj',
            'last_name': 'Kumar',
            'phone': '9876543212',
            'specialization': 'orthopedics',
            'license_number': 'MED003',
            'experience_years': 12,
            'consultation_fee': 1800.00,
            'bio': 'Orthopedic surgeon with expertise in joint replacement and sports injuries.'
        },
        {
            'username': 'dr_sharma',
            'email': 'dr.sharma@medibook.com',
            'first_name': 'Anita',
            'last_name': 'Sharma',
            'phone': '9876543213',
            'specialization': 'pediatrics',
            'license_number': 'MED004',
            'experience_years': 10,
            'consultation_fee': 1000.00,
            'bio': 'Pediatrician dedicated to child healthcare and development.'
        }
    ]
    
    for doctor_data in doctors_data:
        if not User.objects.filter(username=doctor_data['username']).exists():
            user = User.objects.create_user(
                username=doctor_data['username'],
                email=doctor_data['email'],
                password='doctor123',
                first_name=doctor_data['first_name'],
                last_name=doctor_data['last_name'],
                phone=doctor_data['phone'],
                user_type='doctor'
            )
            
            doctor = Doctor.objects.create(
                user=user,
                specialization=doctor_data['specialization'],
                license_number=doctor_data['license_number'],
                experience_years=doctor_data['experience_years'],
                consultation_fee=doctor_data['consultation_fee'],
                bio=doctor_data['bio']
            )
            
            # Create availability for weekdays (Monday to Friday)
            for weekday in range(5):
                DoctorAvailability.objects.create(
                    doctor=doctor,
                    weekday=weekday,
                    start_time=time(9, 0),
                    end_time=time(18, 0)
                )
            
            print(f"Created doctor: Dr. {doctor_data['first_name']} {doctor_data['last_name']}")
    
    # Create sample patients
    patients_data = [
        {
            'username': 'patient1',
            'email': 'patient1@example.com',
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'phone': '9123456789',
            'gender': 'F'
        },
        {
            'username': 'patient2',
            'email': 'patient2@example.com',
            'first_name': 'Bob',
            'last_name': 'Wilson',
            'phone': '9123456788',
            'gender': 'M'
        }
    ]
    
    for patient_data in patients_data:
        if not User.objects.filter(username=patient_data['username']).exists():
            user = User.objects.create_user(
                username=patient_data['username'],
                email=patient_data['email'],
                password='patient123',
                first_name=patient_data['first_name'],
                last_name=patient_data['last_name'],
                phone=patient_data['phone'],
                user_type='patient',
                address='Sample Address, City, State'
            )
            
            Patient.objects.create(
                user=user,
                gender=patient_data['gender']
            )
            
            print(f"Created patient: {patient_data['first_name']} {patient_data['last_name']}")
    
    print("\nSample data created successfully!")
    print("\nLogin credentials:")
    print("Admin: admin / admin123")
    print("Doctors: dr_smith, dr_patel, dr_kumar, dr_sharma / doctor123")
    print("Patients: patient1, patient2 / patient123")

if __name__ == '__main__':
    create_sample_data()
