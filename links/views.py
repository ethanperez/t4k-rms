from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from riders.models import Teammate
from links.models import Link

@login_required
def settings(request):
  # If the form has been submitted
  if request.method == 'POST':
    # Give the post variables a variable
    kintera_id = request.POST['kintera_id']
    t4k_url = request.POST['t4k_url']
    short_link = request.POST['short_link']
  
    # Validate and clean data somewhere here
    # Yaaaaay validations!
    if Link.objects.filter(url = short_link).exists() == True:
      # Link is already in the database
      context = {
        'error_message' : "Sorry, that link has already been taken!",
      }
      # Send them back to the page
      return render(request, 'links/settings.html', context)
    else:
      # Insert into the database
      object = Link.objects.create(user_id = request.user.id, kintera_id = kintera_id, url = short_link, t4k_url = t4k_url)
      object.save()
      context = {
        'success_message' : "You've set your short link successfully!",
      }
      return redirect(reverse('dashboard:dashboard'))
  else:
    # Get the teammate
    tm = Teammate.objects.get(id__exact = request.user.id)
    # Check if the teammate has a short url already
    try:
      Link.objects.get(user_id = tm)
    except ObjectDoesNotExist:
      # They haven't set their link yet
      return render(request, 'links/settings.html')
       
  # What they see if they've already set their short link
  return render(request, 'links/settings_done.html')

@login_required
def stats(request):
  return render(request, 'links/stats.html')