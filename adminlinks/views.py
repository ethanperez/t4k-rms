from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from riders.models import Teammate
from adminlinks.models import Link

def goto(request, dalink):
  # Default
  default = 'http://www.texas4000.org/'

  # See if the link is available
  try:
    lnk = Link.objects.get(short_link = dalink)
  except ObjectDoesNotExist:
    return redirect(default)
  
  # It is a valid link; follow it
  lnk.clicks += 1
  lnk.lask_click = timezone.now()
  lnk.save()
  # redirect
  return redirect(lnk.url)