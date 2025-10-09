from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import User, Doctor, Patient
from datetime import datetime, time


class TimeSlot(models.Model):
    TIME_CHOICES = [
        ('09:00', '09:00 AM'),
        ('09:30', '09:30 AM'),
        ('10:00', '10:00 AM'),
        ('10:30', '10:30 AM'),
        ('11:00', '11:00 AM'),
        ('11:30', '11:30 AM'),
        ('12:00', '12:00 PM'),
        ('14:00', '02:00 PM'),
        ('14:30', '02:30 PM'),
        ('15:00', '03:00 PM'),
        ('15:30', '03:30 PM'),
        ('16:00', '04:00 PM'),
        ('16:30', '04:30 PM'),
        ('17:00', '05:00 PM'),
        ('17:30', '05:30 PM'),
        ('18:00', '06:00 PM'),
    ]
    
    time = models.CharField(max_length=5, choices=TIME_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_time_display()


class DoctorAvailability(models.Model):
    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availability')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('doctor', 'weekday')
    
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError('Start time must be before end time')
    
    def __str__(self):
        return f"Dr. {self.doctor.user.first_name} - {self.get_weekday_display()}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('doctor', 'appointment_date', 'appointment_time')
        ordering = ['-appointment_date', '-appointment_time']
    
    def clean(self):
        # Simple validation - just check if appointment is in the future
        if self.appointment_date < timezone.now().date():
            raise ValidationError('Appointment date cannot be in the past')
    
    def __str__(self):
        return f"{self.patient.user.first_name} - Dr. {self.doctor.user.first_name} ({self.appointment_date})"
    
    @property
    def is_past(self):
        from django.utils import timezone as tz
        appointment_datetime = datetime.combine(
            self.appointment_date,
            datetime.strptime(self.appointment_time.time, '%H:%M').time()
        )
        # Make it timezone aware
        appointment_datetime = tz.make_aware(appointment_datetime)
        return appointment_datetime < tz.now()
    
    @property
    def can_cancel(self):
        return self.status in ['pending', 'confirmed'] and not self.is_past


class AppointmentHistory(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='history')
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=10)
    new_status = models.CharField(max_length=10)
    change_reason = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-changed_at']
    
    def __str__(self):
        return f"{self.appointment} - {self.old_status} to {self.new_status}"
