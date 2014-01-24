from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Avg
from datetime import datetime
import time
from decimal import Decimal
from riders.models import Teammate
from fitness.models import Ride
from django.utils.html import escape

# Base dashboard view
@login_required
def dashboard(request):
    # Retreive total miles
    rides = Ride.objects.filter(user_id__exact = request.user)
    miles = rides.aggregate(Sum('miles'))
    pace = rides.aggregate(Avg('pace'))
    duration = rides.aggregate(Sum('duration'))
    # Return context
    context = {
        'site_title': 'Texas 4000 Rider Management System',
        'page_title': 'Dashboard',
        'navbar_title': 'Texas 4000 RMS',
        'miles': miles,
        'pace': pace,
        'duration': duration,
    }
    return render(request, 'dashboard/index.html', context)

def enter_gate(request):
    # Only execute login logic if data is posted
    if request.method == 'POST':
        # Set user variables
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        # Authenticate the user
        user = authenticate(username = username, password = password)
        # If the user is a user
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard:dashboard'))
            # If the user isn't active
            else:
                # Return context error message
                context = {
                    'site_title': 'Texas 4000 Rider Management System',
                    'page_title': 'Login',
                    'page_header': 'Texas 4000 RMS',
                    'error_message': "You're not an active rider, man."
                }
                return render(request, 'dashboard/login.html', context)
        # If the user doesn't authenticate
        else:
            # Return context error message
            context = {
                'site_title': 'Texas 4000 Rider Management System',
                'page_title': 'Login',
                'page_header': 'Texas 4000 RMS',
                'error_message': "Your username and password don't match!"
            }
            return render(request, 'dashboard/login.html', context)
    # If there's no POST data; just a normal login page
    else:
        # Return context w/ no error
        context = {
            'site_title': 'Texas 4000 Rider Management System',
            'page_title': 'Login',
            'page_header': 'Texas 4000 RMS',
        }
        return render(request, 'dashboard/login.html', context)

# Logout view
def exit_gate(request):
    logout(request)
    return redirect('dashboard:dashboard')
    
# Log a ride
def log_ride(request):
    # If the form has been submitted
    if request.method == 'POST':
        # Give the post variables a variable
        buddies = escape(request.POST['partners'])
        miles = request.POST['miles']
        pace = request.POST['pace']
        time_logged = request.POST['time']
        comments = escape(request.POST['comments'])
        date = request.POST['date']
        # Set the time to the right format
        h = int(time.strftime("%I", time.strptime(time_logged, "%I:%M:%S")))
        m = int(time.strftime("%M", time.strptime(time_logged, "%I:%M:%S")))
        s = int(time.strftime("%S", time.strptime(time_logged, "%I:%M:%S")))
        final_time = (((h*3600)+(m*60)+(s))*1000000)
        
        # Save into the database
        object = Ride.objects.create(user_id = request.user.id, buddies = buddies,
                date = date, miles = Decimal(miles), pace = Decimal(pace),
                duration = final_time, comments = comments)
        object.save()
        # Return to homepage
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    else: # Return an normal page
        context = {
            'site_title': 'Texas 4000 Rider Management System',
            'page_title': 'Log a Ride',
            'navbar_title': 'Texas 4000 RMS',
        }
        return render(request, 'dashboard/add_ride.html', context)

# Change user's password
def change_password(request):
    # If the form has been submitted
    if request.method == 'POST':
        # Check if the passwords match
        if request.POST['password1'] == request.POST['password2'] and request.POST['password2'] is not None:
            # Change the password
            u = Teammate.objects.get(id__exact = request.user.id)
            u.set_password(escape(request.POST['password2']))
            u.save()
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
        else:
           context = {
               'site_title': 'Texas 4000 Rider Management System',
               'page_title': 'Change Password',
               'navbar_title': 'Texas 4000 RMS',
               'error_message': "You're passwords don't match!"
           }
           return render(request, 'dashboard/change_password.html', context)
    else: # First time visitng page
        context = {
            'site_title': 'Texas 4000 Rider Management System',
            'page_title': 'Change Password',
            'navbar_title': 'Texas 4000 RMS',
        }
        return render(request, 'dashboard/change_password.html', context)