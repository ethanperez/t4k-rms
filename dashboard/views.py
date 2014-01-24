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
    # Pass contect to render
    context = {
        'site_title': 'Texas 4000 Rider Management System',
        'page_title': 'Log a Ride',
        'navbar_title': 'Texas 4000 RMS',
    }
    return render(request, 'dashboard/add_ride.html', context)


