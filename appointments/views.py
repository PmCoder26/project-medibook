from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment, Doctor, TimeSlot, DoctorAvailability
from accounts.models import Patient


def dashboard(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'doctor':
            return redirect('appointments:doctor_dashboard')
        else:
            return redirect('appointments:patient_dashboard')
    return redirect('accounts:login')


@login_required
def patient_dashboard(request):
    if request.user.user_type != 'patient':
        return redirect('appointments:doctor_dashboard')
    
    patient = get_object_or_404(Patient, user=request.user)
    from datetime import date
    today = date.today()
    
    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        appointment_date__gte=today,
        status__in=['pending', 'confirmed']
    ).order_by('appointment_date', 'appointment_time')
    
    past_appointments = Appointment.objects.filter(
        patient=patient,
        appointment_date__lt=today
    ).order_by('-appointment_date', '-appointment_time')[:5]
    
    # Calculate counts
    total_appointments = Appointment.objects.filter(
        patient=patient,
        status__in=['pending', 'confirmed', 'completed']
    ).count()
    
    upcoming_count = upcoming_appointments.count()
    past_count = Appointment.objects.filter(
        patient=patient,
        appointment_date__lt=today
    ).count()
    
    context = {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'total_appointments': total_appointments,
        'upcoming_count': upcoming_count,
        'past_count': past_count,
    }
    return render(request, 'appointments/patient_dashboard.html', context)


@login_required
def doctor_dashboard(request):
    if request.user.user_type != 'doctor':
        return redirect('appointments:patient_dashboard')
    
    doctor = get_object_or_404(Doctor, user=request.user)
    from datetime import date
    today = date.today()
    
    today_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=today,
        status__in=['pending', 'confirmed']
    ).order_by('appointment_time')
    
    upcoming_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__gt=today,
        status__in=['pending', 'confirmed']
    ).order_by('appointment_date', 'appointment_time')[:10]
    
    # Calculate counts
    today_count = today_appointments.count()
    upcoming_count = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__gt=today,
        status__in=['pending', 'confirmed']
    ).count()
    
    total_patients = Appointment.objects.filter(
        doctor=doctor,
        status__in=['pending', 'confirmed', 'completed']
    ).values('patient').distinct().count()
    
    context = {
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'today_count': today_count,
        'upcoming_count': upcoming_count,
        'total_patients': total_patients,
    }
    return render(request, 'appointments/doctor_dashboard.html', context)


def doctor_list(request):
    doctors = Doctor.objects.filter(is_available=True).select_related('user')
    specialization = request.GET.get('specialization')
    
    if specialization:
        doctors = doctors.filter(specialization=specialization)
    
    specializations = Doctor.SPECIALIZATION_CHOICES
    
    context = {
        'doctors': doctors,
        'specializations': specializations,
        'selected_specialization': specialization,
    }
    return render(request, 'appointments/doctor_list.html', context)


@login_required
def book_appointment(request, doctor_id):
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can book appointments.')
        return redirect('appointments:doctor_list')
    
    doctor = get_object_or_404(Doctor, id=doctor_id, is_available=True)
    patient = get_object_or_404(Patient, user=request.user)
    
    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        appointment_time_id = request.POST.get('appointment_time')
        symptoms = request.POST.get('symptoms', '')
        
        try:
            appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            appointment_time = get_object_or_404(TimeSlot, id=appointment_time_id)
            
            # Check if slot is available
            existing = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=['pending', 'confirmed']
            ).exists()
            
            if existing:
                messages.error(request, 'This time slot is already booked.')
            else:
                appointment = Appointment.objects.create(
                    patient=patient,
                    doctor=doctor,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time,
                    symptoms=symptoms
                )
                messages.success(request, 'Appointment booked successfully!')
                return redirect('appointments:patient_dashboard')
                
        except Exception as e:
            messages.error(request, 'Error booking appointment. Please try again.')
    
    # Get available time slots
    time_slots = TimeSlot.objects.all()
    
    context = {
        'doctor': doctor,
        'time_slots': time_slots,
    }
    return render(request, 'appointments/book_appointment.html', context)


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check permissions
    if request.user.user_type == 'patient' and appointment.patient.user != request.user:
        messages.error(request, 'You can only cancel your own appointments.')
        return redirect('appointments:patient_dashboard')
    
    if request.user.user_type == 'doctor' and appointment.doctor.user != request.user:
        messages.error(request, 'You can only cancel appointments with your patients.')
        return redirect('appointments:doctor_dashboard')
    
    if appointment.status in ['pending', 'confirmed']:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully.')
    else:
        messages.error(request, 'This appointment cannot be cancelled.')
    
    if request.user.user_type == 'patient':
        return redirect('appointments:patient_dashboard')
    else:
        return redirect('appointments:doctor_dashboard')


@login_required
def update_appointment_status(request, appointment_id):
    if request.user.user_type != 'doctor':
        messages.error(request, 'Only doctors can update appointment status.')
        return redirect('appointments:patient_dashboard')
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if this doctor owns the appointment
    if appointment.doctor.user != request.user:
        messages.error(request, 'You can only update your own appointments.')
        return redirect('appointments:doctor_dashboard')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'confirmed', 'completed', 'cancelled']:
            appointment.status = new_status
            appointment.save()
            messages.success(request, f'Appointment status updated to {new_status}.')
        else:
            messages.error(request, 'Invalid status.')
    
    return redirect('appointments:doctor_dashboard')