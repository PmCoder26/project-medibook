from django.contrib import admin
from .models import TimeSlot, DoctorAvailability, Appointment, AppointmentHistory


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time', 'get_time_display')
    ordering = ('time',)


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'get_weekday_display', 'start_time', 'end_time', 'is_available')
    list_filter = ('weekday', 'is_available')
    search_fields = ('doctor__user__first_name', 'doctor__user__last_name')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'created_at')
    list_filter = ('status', 'appointment_date', 'doctor__specialization')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__first_name', 'doctor__user__last_name')
    date_hierarchy = 'appointment_date'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AppointmentHistory)
class AppointmentHistoryAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'old_status', 'new_status', 'changed_by', 'changed_at')
    list_filter = ('old_status', 'new_status', 'changed_at')
    readonly_fields = ('changed_at',)
