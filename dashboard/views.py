from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Avg
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date
import time
from decimal import Decimal
from riders.models import Teammate
from fitness.models import Ride
from links.models import Link


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
    return render(request, 'dashboard/team_stats.html', context)

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
    
    # Short Link - if it's there
    try:
      link = Link.objects.get(user_id__exact = tm)
    except ObjectDoesNotExist:
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
      
    # Return context
    context = {
        'miles': miles,
        'pace': pace,
        'duration': duration,
        'rides' : rides,
        'rider' : tm,
        'link' : link,
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
                # First login
                tm = Teammate.objects.get(id__exact = request.user.id)
                if tm.first_login == True:
                    # Redirect to first_login page
                    return HttpResponseRedirect(reverse('dashboard:first_login'))
                else:
                    # Redirect straight to the dashboard
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

# Change user's password upon first login
@login_required
def first_login(request):
    # If the form has been submitted
    if request.method == 'POST':
        # Check if the passwords match
        if request.POST['password1'] == request.POST['password2'] and request.POST['password2'] is not None:
            # Change the password and user data
            u = Teammate.objects.get(id__exact = request.user.id)
            u.set_password(request.POST['password2'])
            u.email = request.POST['email']
            u.first_name = request.POST['first_name']
            u.last_name = request.POST['last_name']
            u.title = request.POST['title']
            u.route = request.POST['route']
            u.date_of_birth = request.POST['date_of_birth']
            u.first_login = False
            u.save()
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
        else:
           context = {
               'error_message': "Your passwords don't match!"
           }
           return render(request, 'dashboard/first_login.html', context)
    else: # First time visiting page
        # Get teammate
        tm = Teammate.objects.get(id__exact = request.user.id)
        # Create context
        context = {
            'rider' : tm,
        }
        return render(request, 'dashboard/first_login.html', context)
