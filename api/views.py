from api.decorators import logged_in_or_basicauth
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Avg
from django.http import JsonResponse
from riders.models import Teammate
from fitness.models import Ride
from dashboard.templatetags.datetime_duration import timedelta
from decimal import Decimal
import time, json

@logged_in_or_basicauth()
def account(request):
  if request.method == 'GET':
    mate = Teammate.objects.filter(pk = request.user.pk)
    rides = Ride.objects.filter(user_id = request.user.pk)

    # Ride data
    rideData = {
                'totalMiles': rides.aggregate(Sum('miles'))['miles__sum'],
                'averagePace': '{0:.3}'.format(rides.aggregate(Avg('pace'))['pace__avg']),
                'totalRideTime': timedelta(rides.aggregate(Sum('duration'))['duration__sum'])
    }

    data = {
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'route': request.user.route,
            'dob': request.user.date_of_birth,
            'title': request.user.title,
            'rideData': rideData
            }
    wrapper = {'account': data}
    return JsonResponse(wrapper)

@csrf_exempt
@logged_in_or_basicauth()
def rides(request):
  if request.method == 'GET':
    rides = Ride.objects.filter(user = request.user).order_by('-date')

    data = []
    for ride in rides:
      # Duration to appropriate string
      totalSeconds = ride.duration.seconds
      hours, remainder = divmod(totalSeconds, 3600)
      minutes, seconds = divmod(remainder, 60)
      duration = '%s:%s:%s' % (hours, minutes, seconds)

      rideDict = {
                  'date': ride.date,
                  'buddies': ride.buddies,
                  'miles': ride.miles,
                  'pace': ride.pace,
                  'duation': duration,
                  'comments': ride.comments,
                  'time_logged': ride.time_logged,
      }
      data.append(rideDict)
    
    wrapper = {'rides': data}
    return JsonResponse(wrapper)

  # NOT DUMMY PROOF / NOT VALIDATED
  if request.method == 'POST':
    data = json.loads(request.body)

    new_time = time.strptime(data['time'], "%I:%M:%S")

    h = new_time.tm_hour
    m = new_time.tm_min
    s = new_time.tm_sec

    final_time = (((h*3600) + (m*60) +(s)) * 1000000)
    # Reset time
    data['time'] = final_time

    # Save it
    try:
        object = Ride.objects.create(user_id = request.user.id, buddies = data['buddies'],
            date = data['date'], miles = Decimal(data['miles']), pace = Decimal(data['pace']),
                duration = data['time'], comments = data['comments'])
        object.save()
    except:
         return JsonResponse({'status': '410', 'message': 'Could not save the record'})

    return JsonResponse({'status': '200', 'data': data})