from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import PatientRegistrationForm, DoctorRegistrationForm, LoginForm
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('appointments:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            
            # Redirect based on user type
            if user.user_type == 'doctor':
                return redirect('appointments:doctor_dashboard')
            else:
                return redirect('appointments:patient_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def register_patient(request):
    if request.user.is_authenticated:
        return redirect('appointments:dashboard')
    
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'accounts/register_patient.html', {'form': form})


def register_doctor(request):
    if request.user.is_authenticated:
        return redirect('appointments:dashboard')
    
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Doctor registration successful! Please login.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DoctorRegistrationForm()
    
    return render(request, 'accounts/register_doctor.html', {'form': form})


def register_choice(request):
    if request.user.is_authenticated:
        return redirect('appointments:dashboard')
    return render(request, 'accounts/register_choice.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        # Update basic user information
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        
        # Update date of birth if provided
        dob = request.POST.get('date_of_birth')
        if dob:
            from datetime import datetime
            try:
                user.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
            except:
                pass
        
        # Update address if provided
        address = request.POST.get('address')
        if address:
            user.address = address
            
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile.html', {'user': request.user})
