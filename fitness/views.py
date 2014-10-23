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

def rides(request, rider=None):

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

    return render(request, 'fitness/log.html', context)

@login_required
def log(request):
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
            return render(request, 'fitness/add.html', context)

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
        return HttpResponseRedirect(reverse('fitness:rides'))
    else: # Return an normal page
        return render(request, 'fitness/add.html', {})