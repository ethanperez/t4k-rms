from django.conf.urls import patterns, url
from fitness import views

urlpatterns = patterns('fitness.views',
    url(r'^rides/$', views.rides, name = 'rides'),
)
