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