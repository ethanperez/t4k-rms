from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Avg
from datetime import datetime, date
import time
from decimal import Decimal
from riders.models import Teammate
from fitness.models import Ride


def all_riders(request):
    #TODO maybe we should write a test
    total_miles = Ride.objects.all().aggregate(Sum('miles'))['miles__sum']
    total_time = Ride.objects.all().aggregate(Sum('duration'))['duration__sum']

    #TODO: doing two database joins, this is probably not a good idea in general
    riders = Teammate.objects
    riders = riders.annotate(total_miles = Sum('ride__miles'))
    riders = riders.annotate(total_time = Sum('ride__duration'))
    riders = riders.order_by('-total_miles')
    context = {
        'riders' : riders,
        'total_miles' : total_miles,
        'total_time' : total_time
    }
    return render(request, 'dashboard/all_riders.html', context)

# Base dashboard view
def dashboard(request, rider=None):

    if rider:
        tm = Teammate.objects.get(pk=rider)
    elif not request.user.is_anonymous():
        tm = request.user
    else:
        return HttpResponseRedirect(reverse('dashboard:login'))

    # Retreive total miles
    rides = Ride.objects.filter(user_id__exact = tm).order_by('-date')
    miles = rides.aggregate(Sum('miles'))
    pace = rides.aggregate(Avg('pace'))
    duration = rides.aggregate(Sum('duration'))

    # Return context
    context = {
        'miles': miles,
        'pace': pace,
        'duration': duration,
        'rides' : rides,
        'rider' : tm,
        'import_date' : date(2014,01,26),
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
                    'error_message': "You're not an active rider, man."
                }
                return render(request, 'dashboard/login.html', context)
        # If the user doesn't authenticate
        else:
            # Return context error message
            context = {
                'error_message': "Your username and password don't match!"
            }
            return render(request, 'dashboard/login.html', context)
    # If there's no POST data; just a normal login page
    else:
        # Return context w/ no error
        return render(request, 'dashboard/login.html', {})

# Logout view
def exit_gate(request):
    logout(request)
    return redirect('dashboard:dashboard')

# Log a ride
@login_required
def log_ride(request):
    # If the form has been submitted
    if request.method == 'POST':
        # Give the post variables a variable
        buddies = request.POST['partners']
        miles = request.POST['miles']
        pace = request.POST['pace']
        time_logged = request.POST['time']
        comments = request.POST['comments']
        date = request.POST['date']

        new_time = None
        try:
            new_time = time.strptime(time_logged, "%I:%M:%S")
        except ValueError:
            context = {
              'buddies' : buddies,
              'miles' : miles,
              'pace' : pace,
              'comments' : comments,
              'ride_date' : date,
              'time_logged_error' : "Invalid time format. Use HH:MM:SS",
            }
            return render(request, 'dashboard/add_ride.html', context)

        # Set the time to the right format
        h = new_time.tm_hour
        m = new_time.tm_min
        s = new_time.tm_sec

        #TODO do we need to do this
        final_time = (((h*3600)+(m*60)+(s))*1000000)

        # Save into the database
        object = Ride.objects.create(user_id = request.user.id, buddies = buddies,
                date = date, miles = Decimal(miles), pace = Decimal(pace),
                duration = final_time, comments = comments)
        object.save()
        # Return to homepage
        return HttpResponseRedirect(reverse('dashboard:dashboard'))
    else: # Return an normal page
        return render(request, 'dashboard/add_ride.html', {})

# Change user's password
@login_required
def change_password(request):
    # If the form has been submitted
    if request.method == 'POST':
        # Check if the passwords match
        if request.POST['password1'] == request.POST['password2'] and request.POST['password2'] is not None:
            # Change the password
            u = Teammate.objects.get(id__exact = request.user.id)
            u.set_password(request.POST['password2'])
            u.save()
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
        else:
           context = {
               'error_message': "Your passwords don't match!"
           }
           return render(request, 'dashboard/change_password.html', context)
    else: # First time visiting page
        return render(request, 'dashboard/change_password.html', {})
